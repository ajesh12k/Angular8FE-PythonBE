import { Component, OnInit } from '@angular/core';
import { DataShareService } from '../data-share.service';
import {CookieService} from 'ngx-cookie-service';
import {NavigationEnd, Router} from '@angular/router';
import {ShowMessageService} from '../show-message.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  homeComponentItems: any = {};
  showLogin: boolean;
  showRegister: boolean;
  mySubscription: any;
  constructor(private data: DataShareService,
              public cookieService: CookieService,
              private router: Router,
              public showMessageService: ShowMessageService) {
    // tslint:disable-next-line:only-arrow-functions
    this.router.routeReuseStrategy.shouldReuseRoute = function() {
      return false;
    };
    this.mySubscription = this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        // Trick the Router into believing it's last link wasn't previously loaded
        this.router.navigated = false;
      }
    });
  }
  ngOnInit() {
    this.data.currentMessage.subscribe(message => this.homeComponentItems = message);
    if (!this.showLogin) {
      this.showLogin = false;
    }
    if (!this.showRegister) {
      this.showRegister = false;
    }
    this.showLoginOn();
  }
  //
  showLoginOff() {
    // console.log('Inside showLoginOff');
    this.showLogin = false;
  }
  //
  showLoginOn() {
    // console.log('Inside showLoginOn');
    this.showLogin = true;
  }
   //
  showRegisterOff() {
    // console.log('Inside showRegisterOff');
    this.showRegister = false;
  }
  //
  showRegisterOn() {
    // console.log('Inside showRegisterOn');
    this.showRegister = true;
  }
}


