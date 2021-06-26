import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';


export interface Config {
  heroesUrl: string;
  textfile: string;
  error_list:any;
  Finnish:string;
  
}

@Injectable()
export class ConfigService {

configUrl='/assets/config.json';

  constructor(private http: HttpClient) { }

  getData() {
    return this.http.get<Config>(this.configUrl); 
  }
}

//Check here fro more information https://angular.io/guide/http 

//** Please check how Observable work


//Check for retrieve json data array here : http://choly.ca/post/typescript-json/