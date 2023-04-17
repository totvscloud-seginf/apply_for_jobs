export interface IPassword {
    password: string;
    view_limit: number;
    valid_until: number;
}

export const setPassword = async (password: IPassword, apiUrl: string) : Promise<any> => {
    return new Promise((resolve, reject) => {
        fetch(`${apiUrl}/password`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(password),
        }).then((response) => {
            if(response.status !== 201) {
                reject(response);
            }
            resolve(response.json());
        }).catch((error) => {
            reject(error);
        });
    });
}
