import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DataShareService {
  //
  private messageSource = new BehaviorSubject('');
  private navigationHeaders = new BehaviorSubject('');
  private questionPage = new BehaviorSubject('');
  private selectedLanguage = new BehaviorSubject('');
  private registerPage = new BehaviorSubject('');
  private loginPage = new BehaviorSubject('');
  private loginResult = new BehaviorSubject('');
  private feedbackPage = new BehaviorSubject('');
  private infoPage = new BehaviorSubject('');
  private faqPage = new BehaviorSubject('');
  private forgetPasswordPage = new BehaviorSubject('');
  private resetPasswordPage = new BehaviorSubject('');
  private changePasswordPage = new BehaviorSubject('');
  private userDeviceInfo = new BehaviorSubject('');
  private errorMessageList = new BehaviorSubject('');
  private successMessageList = new BehaviorSubject('');
  //
  currentMessage = this.messageSource.asObservable();
  navigationItems = this.navigationHeaders.asObservable();
  questionPageStatic = this.questionPage.asObservable();
  registerPageStatic = this.registerPage.asObservable();
  loginPageStatic = this.loginPage.asObservable();
  userLoginResult = this.loginResult.asObservable();
  feedbackPageStatic = this.feedbackPage.asObservable();
  currentLanguage = this.selectedLanguage.asObservable();
  infoPageStatic = this.infoPage.asObservable();
  faqPageStatic = this.faqPage.asObservable();
  forgetPageStatic = this.forgetPasswordPage.asObservable();
  resetPageStatic = this.resetPasswordPage.asObservable();
  changePageStatic = this.changePasswordPage.asObservable();
  userDeviceInfoStatic = this.userDeviceInfo.asObservable();
  errorMessageListStatic = this.errorMessageList.asObservable();
  successMessageListStatic = this.successMessageList.asObservable();

  //
  constructor() { }
  //
  changeMessage(message: string) {
    this.messageSource.next(message);
  }
  //
  changeNavigation(message: string) {
    this.navigationHeaders.next(message);
  }
  //
  changeLanguage(language: string) {
    this.selectedLanguage.next(language);
  }
  //
  changeRegisterPageStatic(message: string) {
    this.registerPage.next(message);
  }
  //
  changeLoginPageStatic(message: string) {
    this.loginPage.next(message);
  }
  //
  storeLoginResult(message: string) {
    this.loginResult.next(message);
  }
  //
  changeFeedbackPageStatic(message: string) {
    this.feedbackPage.next(message);
  }
  //
  changeQuestionPageStatic(message: string) {
    this.questionPage.next(message);
  }
  //
  changeInfoPageStatic(message: string) {
   this.infoPage.next(message);
  }
  //
  changeFaqPageStatic(message: string) {
    this.faqPage.next(message);
  }
  //
  changeForgetPasswordPageStatic(message: string) {
    this.forgetPasswordPage.next(message);
  }
  //
  changeResetPasswordPageStatic(message: string) {
    this.resetPasswordPage.next(message);
  }
  //
  changeChangePasswordPageStatic(message: string) {
    this.changePasswordPage.next(message);
  }
  //
  storeUserDeviceInfoStatic(message: string) {
    this.userDeviceInfo.next(message);
  }
   //
  storeErrorMessageListStatic(message: string) {
    this.errorMessageList.next(message);
  }
  //
  storeSuccessMessageListStatic(message: string) {
    this.successMessageList.next(message);
  }
}
