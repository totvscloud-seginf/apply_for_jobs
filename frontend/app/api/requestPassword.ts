export const requestPassword = async (id: string, apiUrl: string) : Promise<any> => {
    return new Promise((resolve, reject) => {
        fetch(`${apiUrl}/password/${id}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        }).then((response) => {
            if(response.status !== 200) {
                reject(response);
            }
            resolve( response.json() );
        }).catch((error) => {
            reject(error);
        });
    });
}
