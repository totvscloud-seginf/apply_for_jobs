import { useState } from 'react';
import axios from 'axios';


function useRequest() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);


  const makeRequest = async (params) => {
    let config = {
      method: 'POST',
      maxBodyLength: Infinity,
      url: params.url,
      headers: { 
        'Acess-Control-Allow-Origin' : '*',
        'Content-Type': 'application/json', 
        'X-Amz-Content-Sha256': 'beaead3198f7da1e70d03ab969765e0821b24fc913697e929e726aeaebf0eba3', 
        'X-Amz-Date': '20230419T163422Z', 
        'Authorization': 'AWS4-HMAC-SHA256 Credential=AKIAROLDIRS6GS7JQGWW/20230419/sa-east-1/execute-api/aws4_request, SignedHeaders=content-length;content-type;host;x-amz-content-sha256;x-amz-date, Signature=d1210305c60e96e19cb692fd5f09d5d1ccbb0ddf14eaa4a8181d4c71da52a2cc'
      },
      data : params.data
    };
  
    try {

      const response = await axios.request(config);

      if ('result' in response) {
        const result = response['result'];
        if (result !== 'OK') {
          setData(response.data);
          throw new Error('Erro na requisição');
        }
      }

      setData(response.data);
      setLoading(false);
      return response.data;
      } catch (error) {
        setLoading(false);
        setError(error);
        throw error;
        }
    };
  
    return { data, error, loading, makeRequest };
}

export default useRequest;