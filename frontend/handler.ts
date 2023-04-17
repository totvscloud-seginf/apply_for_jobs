import "source-map-support/register";
import { Context, APIGatewayEvent, APIGatewayProxyResultV2 } from "aws-lambda";

export const serve = async (event: APIGatewayEvent, _context: Context): Promise<APIGatewayProxyResultV2> => {

  try {
    // We use asynchronous import here so we can better catch server-side errors during development
    const render = (await import("./src/server/render")).default;
    if(event.resource === "/password/{id}") {
      const id = event.pathParameters?.id;
      if(id && /^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(id)) {
        return {
          statusCode: 200,
          headers: {
            "Content-Type": "text/html",
          },
          body: await render(event, {..._context, password: id}),
        };
      }
    }

    return {
      statusCode: 200,
      headers: {
        "Content-Type": "text/html",
      },
      body: await render(event),
    };
  } catch (error) {
    // Custom error handling for server-side errors
    // TODO: Prettify the output, include the callstack, e.g. by using `youch` to generate beautiful error pages
    console.error(error);
    return {
      statusCode: 500,
      headers: {
        "Content-Type": "text/html",
      },
      body: `<html><body>${error.toString()}</body></html>`,
    };
  }
};