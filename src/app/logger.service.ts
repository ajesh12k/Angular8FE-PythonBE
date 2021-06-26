import { Injectable } from '@angular/core';

export enum LogLevel {
  All = 0,
  Debug = 1,
  Info = 2,
  Warn = 3,
  Error = 4,
  Fatal = 5,
  Off = 6
}

@Injectable({
  providedIn: 'root'
})
export class LogService {
level: LogLevel = LogLevel.All;
logWithDate: boolean = true;


  log(msg: any) {
    console.log(new Date() + ": "
      + JSON.stringify(msg));
  }
}
