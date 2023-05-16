import React from "react";
import App from "./App";

class Password extends App {

    constructor(props){
        super(props);

        this.state = {
            passwords: [
                {
                'id': 1,
                'email': '', 
                'password': '', 
                'views': '', 
                'time_views': '',
                'url': '',
                'expire': false,
                'date_free': '',
                'last_updated': '',
                'use_characters': false,
                'use_numbers': false,
                'use_words': false,
                'pass_size': false
                }
            ]
        }
    }

}