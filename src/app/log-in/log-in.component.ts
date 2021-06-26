import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {WebserviceCallerService} from '../webservice-caller.service';
import {ActivatedRoute, Router} from '@angular/router';
import {DataShareService} from '../data-share.service';
import {CookieService} from 'ngx-cookie-service';
import {HomeComponent} from '../home/home.component';
import {ShowMessageService} from '../show-message.service';
import {MatSnackBar} from '@angular/material/snack-bar';

@Component({
  selector: 'app-log-in',
  templateUrl: './log-in.component.html',
  styleUrls: ['./log-in.component.css']
})
export class LogInComponent implements OnInit {

  loginComponentItems: any = {};
  navComponentItems: any = {};
  userDeviceInfo: any = {};
  public selectedLanguage: string;
  formLogin: FormGroup;
  errorMsg: any = {};
  showUserFieldError: any = {};
  showPasswordFieldError: any = {};
  showEmailFieldError: any = {};
  successMsg: any = {};
  public userLoginRequest = {
    mtee_user_id: undefined,
    mtee_user_pwd: undefined,
    mtee_user_device_info: undefined,
  };
  public loginResult: any;
  //
  constructor(public rest: WebserviceCallerService,
              private route: ActivatedRoute,
              private router: Router,
              private dataBus: DataShareService,
              private formBuilder: FormBuilder,
              public cookieService: CookieService,
              public homeComponent: HomeComponent,
              public showMessageService: ShowMessageService,
              public snackBar: MatSnackBar) {
  }
  //
  //
  ngOnInit() {
    this.dataBus.loginPageStatic.subscribe(message => this.loginComponentItems = message);
    this.dataBus.navigationItems.subscribe(message => this.navComponentItems = message);
    this.dataBus.currentLanguage.subscribe(language => this.selectedLanguage = language);
    // console.log(this.loginComponentItems);
    this.formLogin = this.formBuilder.group({
      mtee_user_id: [null, Validators.compose([Validators.required, Validators.minLength(4), Validators.maxLength(40)])],
      mtee_user_pwd: [null, Validators.compose([Validators.required, Validators.minLength(6), Validators.maxLength(40)])]
    });
  }
  //
loginUser() {
    if (this.formLogin.value.mtee_user_id !== '' &&  this.formLogin.value.mtee_user_pwd !== '') {
          this.userLoginRequest.mtee_user_id = this.formLogin.value.mtee_user_id;
          // console.log(this.userLoginRequest.mtee_user_id);
          //
          this.userLoginRequest.mtee_user_pwd = btoa(this.formLogin.value.mtee_user_pwd);
          // console.log(this.userLoginRequest.mtee_user_pwd);
          this.dataBus.userDeviceInfoStatic.subscribe(message => this.userDeviceInfo = message);
          // console.log('D E V I C E     I N F O ');
          // console.log(this.userDeviceInfo);
          this.userLoginRequest.mtee_user_device_info = this.userDeviceInfo;
          this.rest.loginUser(this.userLoginRequest)
            .subscribe(data => {
              if ( data.status === 'success') {
                // console.log(' Data From Validate User: ');
                // this.cookieService.set('UserId', this.userLoginRequest.mtee_user_id);
                // @ts-ignore
                this.cookieService.set('UserId', this.userLoginRequest.mtee_user_id, undefined, '/', undefined, false);
                localStorage.setItem('UserId', this.userLoginRequest.mtee_user_id);
                this.loginResult = data.result[0];
                this.dataBus.storeLoginResult(this.loginResult);
                // console.log(data.result[0].mtee_user_role);
                this.successMsg = this.showMessageService.getSuccessMessageByCode('903');
                this.showSuccessMessageSnackBar();
                if (data.result[0].mtee_user_role === 'T') {
                  this.router.navigate(['questions']);
                } else {
                  this.router.navigate(['settings']);
                }
              } else {
                // showing direct error message from service
                this.errorMsg = data.result.mtee_message_text;
                this.showErrorMessageSnackBar();
              }
            });
    } else {
      this.errorMsg = this.showMessageService.getErrorMessageByCode('106');
      this.showErrorMessageSnackBar();
    }

  }
  //
  //
  registerUserClicked() {
    // this.cookieService.set('UserId', '*');
    this.cookieService.set('UserId', '*', undefined, '/', undefined, true);
    localStorage.setItem('UserId', '*');
    this.homeComponent.showLoginOff();
    this.homeComponent.showRegisterOn();
  }
  //
  showSuccessMessageSnackBar() {
    this.snackBar.open(this.successMsg[this.selectedLanguage], '', {
                  verticalPosition: 'bottom', horizontalPosition: 'center', panelClass: ['successSnackbar'], duration : 3000
                });
  }
  //
  showErrorMessageSnackBar() {
    this.snackBar.open(this.errorMsg[this.selectedLanguage], '', {
        verticalPosition: 'bottom', horizontalPosition: 'center', panelClass: ['errorSnackbar'], duration : 5000
      });
  }
  //
  getFormErrorTextUser() {
    // console.log('getFormErrorTextUser');
    this.showUserFieldError = this.showMessageService.getErrorMessageByCode('115');
    this.errorMsg = this.showUserFieldError;
    // console.log(this.errorMsg);
    return this.errorMsg[this.selectedLanguage];
  }
  //
  getFormErrorTextPassword() {
    // console.log('getFormErrorTextPassword');
    this.showPasswordFieldError = this.showMessageService.getErrorMessageByCode('116');
    this.errorMsg = this.showPasswordFieldError;
    // console.log(this.errorMsg);
    return this.errorMsg[this.selectedLanguage];
  }
  //
}
