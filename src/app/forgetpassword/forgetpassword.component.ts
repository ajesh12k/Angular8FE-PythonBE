import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators, FormControl } from '@angular/forms';
import { WebserviceCallerService } from '../webservice-caller.service';
import { DataShareService } from '../data-share.service';
import {ActivatedRoute, Router} from '@angular/router';
import {CookieService} from 'ngx-cookie-service';
import {ShowMessageService} from '../show-message.service';
import {MatSnackBar} from '@angular/material/snack-bar';

@Component({
  selector: 'app-forgetpassword',
  templateUrl: './forgetpassword.component.html',
  styleUrls: ['./forgetpassword.component.scss']
})
export class ForgetpasswordComponent implements OnInit {
 formRecovery: FormGroup;
  errorMsg: any = {};
  successMsg: any = {};
  showUserFieldError: any = {};
  public userRecoveryRequest = {
    mtee_user_id: undefined,
    mtee_user_lang: undefined
  };
  forgetPasswordComponentItems: any = {};
  public selectedLanguage: string;
  private showEmailFieldError: any;
  constructor( private formBuilder: FormBuilder,
               public rest: WebserviceCallerService,
               private route: ActivatedRoute,
               public cookieService: CookieService,
               private router: Router,
               private data: DataShareService,
               public showMessageService: ShowMessageService,
               public snackBar: MatSnackBar) {}

  ngOnInit() {
    this.formRecovery = this.formBuilder.group({
      username: [null, Validators.compose([Validators.required, Validators.email])]
    });
    this.data.forgetPageStatic.subscribe(message => this.forgetPasswordComponentItems = message);
    this.data.currentLanguage.subscribe(language => this.selectedLanguage = language);
  }
  //
  recoverUser() {
    this.userRecoveryRequest.mtee_user_id = this.formRecovery.value.username;
    this.userRecoveryRequest.mtee_user_lang = this.selectedLanguage;
    // console.log(this.userRecoveryRequest);
    this.rest.recoverUser(this.userRecoveryRequest)
    .subscribe(data => {
        console.log(data);
        if ( data.status === 'success') {
          this.successMsg = this.showMessageService.getSuccessMessageByCode('906');
          this.snackBar.open(this.successMsg[this.selectedLanguage], '', {
                  verticalPosition: 'bottom', horizontalPosition: 'center', panelClass: ['successSnackbar'], duration : 3000
          });
        } else {
          this.errorMsg = this.showMessageService.getErrorMessageByCode('119');
          this.snackBar.open(this.errorMsg[this.selectedLanguage], '', {
                  verticalPosition: 'bottom', horizontalPosition: 'center', panelClass: ['errorSnackbar'], duration : 3000
          });
        }
    });
  }
  //
  getFormErrorTextUser() {
    this.showUserFieldError = this.showMessageService.getErrorMessageByCode('115');
    this.errorMsg = this.showUserFieldError;
    return this.errorMsg[this.selectedLanguage];
  }
  //
  //
  getFormErrorTextEmail() {
    console.log('getFormErrorTextEmail');
    this.showEmailFieldError = this.showMessageService.getErrorMessageByCode('103');
    this.errorMsg = this.showEmailFieldError;
    console.log(this.errorMsg);
    return this.errorMsg[this.selectedLanguage];
  }
}
