import {Component, OnInit} from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { WebserviceCallerService } from './webservice-caller.service';
import { ActivatedRoute, Router } from '@angular/router';
import {DataShareService} from './data-share.service';
import {CookieService} from 'ngx-cookie-service';
import { DeviceDetectorService } from 'ngx-device-detector';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent implements OnInit {
  title = '  FIN MTEE';
  staticPageContent: any = [];
  languageList: any = [];
  selectedLanguage = 'Finnish';
  mapComponentList: any = [];
  navComponentItems: any = {};
  homeComponentItems: any = {};
  questionComponentItems: any = {};
  loginComponentItems: any = {};
  registerComponentItems: any = {};
  feedbackComponentItems: any = {};
  forgetPasswordComponentItems: any = {};
  resetPasswordComponentItems: any = {};
  changePasswordComponentItems: any = {};
  activateUserComponentItems: any = {};
  infoComponentItems: any = {};
  faqComponentItems: any = {};
  ComponentListByLang: any = [];
  ComponentListAll: any = [];
  DataTransferMessage: any = [];
  public userLoginDetails: any = {};
  private deviceInfo: any;
  errorList: any = [];
  successMessageList: any = [];

  // tslint:disable-next-line:max-line-length
  constructor(public rest: WebserviceCallerService,
              private route: ActivatedRoute,
              private router: Router,
              private dataBus: DataShareService,
              private deviceService: DeviceDetectorService,
              public cookieService: CookieService) { }

  ngOnInit() {
    // console.log('Inside ngOnInit in app component caller');
    this.selectedLanguage = 'Finnish';
    this.getAllLanguage();
    this.getErrorList();
    this.getSuccessMessageList();
    this.dataBus.userLoginResult.subscribe(message => this.userLoginDetails = message);
    // console.log(this.userLoginDetails.mtee_user_id);
    this.deviceInfo = this.deviceService.getDeviceInfo();
    // console.log('D E V I C E     I N F O ');
    // console.log(this.deviceInfo);
    // console.log('Calling storeUserDeviceInfoStatic ');
    // this.saveUserAccessDetails();
    this.dataBus.storeUserDeviceInfoStatic(this.deviceInfo);
  }


  async delay(ms: number) {
    await new Promise(resolve => setTimeout(() => resolve(), ms)).then(() => console.log('fired'));
  }
  //
  saveUserAccessDetails() {
  if (localStorage.getItem('*') !== '*') {
     // console.log('Calling storeUserDeviceInfoStatic ');
     this.rest.saveUserAccessDetails(this.deviceInfo).subscribe((data: {}) => {
     localStorage.setItem('*', '*');
     });
  }
  }
  //
  getAllLanguage() {
    // console.log('Inside getAllLanguage in app component caller');
    this.languageList = [];
    this.rest.getAllLanguage().subscribe
    (
      (data: {}) => {
        // console.log('logging language data');
        // console.log(data);
        this.languageList = data;
        this.getAllStaticContent();
      }
      );
  }
//
  getSuccessMessageList() {
    // console.log('Inside getSuccessMessageList in app component caller');
    this.successMessageList = [];
    this.rest.getSuccessMessageList().subscribe
    (
      (data: {}) => {
        // console.log('logging Success Message data');
        this.successMessageList = data;
        // console.log(this.successMessageList);
        this.dataBus.storeSuccessMessageListStatic(this.successMessageList);
      }
      );
  }
  //
  getErrorList() {
    // console.log('Inside getErrorList in app component caller');
    this.errorList = [];
    this.rest.getErrorList().subscribe
    (
      (data: {}) => {
        // console.log('logging Error data');
        this.errorList = data;
        // console.log(this.errorList);
        this.dataBus.storeErrorMessageListStatic(this.errorList);
      }
      );
  }
  //
  getAllStaticContent() {
    // console.log('Inside getAllStaticContent in app component caller');
    this.staticPageContent = [];
    this.mapComponentList = [];
    this.rest.getAllStaticContent().subscribe
    ((data: {}) => {
        // console.log('logging static content');
        // console.log(data);
        this.mapStaticData(data, this.selectedLanguage, this.languageList, this.ComponentListAll, this.ComponentListByLang);
        this.staticPageContent = data;
        this.dataBus.changeLanguage(this.selectedLanguage);
        this.switchLanguage(this.selectedLanguage, this.ComponentListAll);
        this.dataBus.changeNavigation(this.navComponentItems);
        this.dataBus.changeMessage(this.homeComponentItems);
        this.dataBus.changeQuestionPageStatic(this.questionComponentItems);
        this.dataBus.changeRegisterPageStatic(this.registerComponentItems);
        this.dataBus.changeLoginPageStatic(this.loginComponentItems);
        this.dataBus.changeFeedbackPageStatic(this.feedbackComponentItems);
        this.dataBus.changeInfoPageStatic(this.infoComponentItems);
        this.dataBus.changeFaqPageStatic(this.faqComponentItems);
        this.dataBus.changeForgetPasswordPageStatic(this.forgetPasswordComponentItems);
        this.dataBus.changeResetPasswordPageStatic(this.resetPasswordComponentItems);
        this.dataBus.changeChangePasswordPageStatic(this.changePasswordComponentItems);
      }
    );
  }

  onSelectionChange(lang) {
    // console.log('----language--:', lang.value);
    this.selectedLanguage = lang.value;
    this.dataBus.changeLanguage(this.selectedLanguage);
    this.switchLanguage(this.selectedLanguage, this.ComponentListAll);
    this.dataBus.changeMessage(this.homeComponentItems);
    this.dataBus.changeQuestionPageStatic(this.questionComponentItems);
  }

  switchLanguage(selectedLanguage, ComponentListAll) {
    // console.log('-----static list switcher map : ', selectedLanguage);
    switch (selectedLanguage) {
      case 'Swedish':
        this.replaceLanguageText(selectedLanguage, ComponentListAll);
        break;
        case 'English':
          this.replaceLanguageText(selectedLanguage, ComponentListAll);
          break;
          case 'Finnish':
            default:
              this.replaceLanguageText(selectedLanguage, ComponentListAll);
              break;
    }
  }
replaceLanguageText(selectedLanguage, ComponentListAll) {
          this.navComponentItems.info = ComponentListAll[0].component_list.language_list[selectedLanguage][0];
          this.navComponentItems.faq = ComponentListAll[0].component_list.language_list[selectedLanguage][1];
          this.navComponentItems.admin = ComponentListAll[0].component_list.language_list[selectedLanguage][2];
          this.navComponentItems.login = ComponentListAll[0].component_list.language_list[selectedLanguage][4];
          this.navComponentItems.register = ComponentListAll[0].component_list.language_list[selectedLanguage][5];
          this.navComponentItems.feedback = ComponentListAll[0].component_list.language_list[selectedLanguage][6];
          this.navComponentItems.questions = ComponentListAll[0].component_list.language_list[selectedLanguage][7];
          this.navComponentItems.changepwd = ComponentListAll[0].component_list.language_list[selectedLanguage][8];
          this.navComponentItems.logout = ComponentListAll[0].component_list.language_list[selectedLanguage][9];
          //
          this.homeComponentItems.mtee_app_tagline = ComponentListAll[1].component_list.language_list[selectedLanguage][0];
          this.homeComponentItems.tabcontent = ComponentListAll[1].component_list.language_list[selectedLanguage][2];
          this.homeComponentItems.mtee_funding_messaging = ComponentListAll[1].component_list.language_list[selectedLanguage][3];
          this.homeComponentItems.startbutton = ComponentListAll[1].component_list.language_list[selectedLanguage][4];
          //
          this.loginComponentItems.mtee_login_tigline = ComponentListAll[2].component_list.language_list[selectedLanguage][0];
          this.loginComponentItems.mtee_user_id = ComponentListAll[2].component_list.language_list[selectedLanguage][1];
          this.loginComponentItems.mtee_user_id_plchldr = ComponentListAll[2].component_list.language_list[selectedLanguage][2];
          this.loginComponentItems.mtee_user_pwd = ComponentListAll[2].component_list.language_list[selectedLanguage][3];
          this.loginComponentItems.mtee_user_pwd_plchldr = ComponentListAll[2].component_list.language_list[selectedLanguage][4];
          this.loginComponentItems.mtee_login_btn = ComponentListAll[2].component_list.language_list[selectedLanguage][5];
          this.loginComponentItems.mtee_forgot_pwd_btn = ComponentListAll[2].component_list.language_list[selectedLanguage][6];
          //
          this.registerComponentItems.registerTagline = ComponentListAll[3].component_list.language_list[selectedLanguage][0];
          this.registerComponentItems.mtee_user_yob = ComponentListAll[3].component_list.language_list[selectedLanguage][1];
          this.registerComponentItems.mtee_user_gender = ComponentListAll[3].component_list.language_list[selectedLanguage][2];
          this.registerComponentItems.mtee_user_id = ComponentListAll[3].component_list.language_list[selectedLanguage][3];
          this.registerComponentItems.mtee_user_id_plchldr = ComponentListAll[3].component_list.language_list[selectedLanguage][4];
          this.registerComponentItems.mtee_user_pwd = ComponentListAll[3].component_list.language_list[selectedLanguage][5];
          this.registerComponentItems.mtee_user_pwd_plchldr = ComponentListAll[3].component_list.language_list[selectedLanguage][6];
          this.registerComponentItems.mtee_user_email = ComponentListAll[3].component_list.language_list[selectedLanguage][7];
          this.registerComponentItems.mtee_user_email_plchldr = ComponentListAll[3].component_list.language_list[selectedLanguage][8];
          this.registerComponentItems.mtee_reset_register_btn = ComponentListAll[3].component_list.language_list[selectedLanguage][9];
          this.registerComponentItems.mtee_register_form_btn = ComponentListAll[3].component_list.language_list[selectedLanguage][10];
          //
          this.questionComponentItems.questionInstruction = ComponentListAll[4].component_list.language_list[selectedLanguage][0];
          this.questionComponentItems.campaignCode = ComponentListAll[4].component_list.language_list[selectedLanguage][10];
          this.questionComponentItems.campaignCodePlaceHolder = ComponentListAll[4].component_list.language_list[selectedLanguage][11];
          this.questionComponentItems.backButton = ComponentListAll[4].component_list.language_list[selectedLanguage][9];
          // this.questionComponentItems.mtee_next_btn = ComponentListAll[4].component_list.language_list[selectedLanguage][14];
          this.questionComponentItems.nextButton = ComponentListAll[4].component_list.language_list[selectedLanguage][10];
          this.questionComponentItems.submitButton = ComponentListAll[4].component_list.language_list[selectedLanguage][11];
          //
          this.feedbackComponentItems.mtee_feedback_tagline = ComponentListAll[5].component_list.language_list[selectedLanguage][0];
          this.feedbackComponentItems.mtee_feedback_explanation = ComponentListAll[5].component_list.language_list[selectedLanguage][1];
          this.feedbackComponentItems.mtee_feedback_instruction = ComponentListAll[5].component_list.language_list[selectedLanguage][2];
          this.feedbackComponentItems.mtee_feedback_responses = ComponentListAll[5].component_list.language_list[selectedLanguage][3];
          this.feedbackComponentItems.mtee_feedback_details = ComponentListAll[5].component_list.language_list[selectedLanguage][4];
          // info
          this.infoComponentItems.mtee_app_info_header = ComponentListAll[6].component_list.language_list[selectedLanguage][0];
          this.infoComponentItems.mtee_app_infoText1 = ComponentListAll[6].component_list.language_list[selectedLanguage][1];
          this.infoComponentItems.mtee_app_infoText2 = ComponentListAll[6].component_list.language_list[selectedLanguage][2];
          this.infoComponentItems.mtee_app_infoText3 = ComponentListAll[6].component_list.language_list[selectedLanguage][3];
          this.infoComponentItems.mtee_app_infoContact1 = ComponentListAll[6].component_list.language_list[selectedLanguage][4];
          this.infoComponentItems.mtee_app_infoContact2 = ComponentListAll[6].component_list.language_list[selectedLanguage][5];
          this.infoComponentItems.mtee_app_infoContact3 = ComponentListAll[6].component_list.language_list[selectedLanguage][6];
          this.infoComponentItems.mtee_app_infoDataSecurity = ComponentListAll[6].component_list.language_list[selectedLanguage][7];
          this.infoComponentItems.mtee_app_info_datasecurity_btn = ComponentListAll[6].component_list.language_list[selectedLanguage][8];
          // faq
          this.faqComponentItems.mtee_app_faq_header = ComponentListAll[7].component_list.language_list[selectedLanguage][0];
          // forget_password
          this.forgetPasswordComponentItems.mtee_app_fp_header = ComponentListAll[8].component_list.language_list[selectedLanguage][0];
          this.forgetPasswordComponentItems.mtee_app_fp_instruction = ComponentListAll[8].component_list.language_list[selectedLanguage][1];
          this.forgetPasswordComponentItems.mtee_app_fp_eml_plchldr = ComponentListAll[8].component_list.language_list[selectedLanguage][2];
          this.forgetPasswordComponentItems.mtee_app_fp_reset_btn = ComponentListAll[8].component_list.language_list[selectedLanguage][3];
          // reset_password
          this.resetPasswordComponentItems.mtee_app_rp_header = ComponentListAll[9].component_list.language_list[selectedLanguage][0];
          this.resetPasswordComponentItems.mtee_app_rp_new = ComponentListAll[9].component_list.language_list[selectedLanguage][1];
          this.resetPasswordComponentItems.mtee_app_rp_confirm = ComponentListAll[9].component_list.language_list[selectedLanguage][2];
          this.resetPasswordComponentItems.mtee_app_rp_save_btn = ComponentListAll[9].component_list.language_list[selectedLanguage][3];
          // change_password
          this.changePasswordComponentItems.mtee_app_cp_header = ComponentListAll[10].component_list.language_list[selectedLanguage][0];
          this.changePasswordComponentItems.mtee_app_cp_old = ComponentListAll[10].component_list.language_list[selectedLanguage][1];
          this.changePasswordComponentItems.mtee_app_cp_new = ComponentListAll[10].component_list.language_list[selectedLanguage][2];
          this.changePasswordComponentItems.mtee_app_cp_confirm = ComponentListAll[10].component_list.language_list[selectedLanguage][3];
          this.changePasswordComponentItems.mtee_app_cp_save_btn = ComponentListAll[10].component_list.language_list[selectedLanguage][4];
  }
  // This function creates a array of static content using language as key. The array constructed is dynamic.
  //       [{"ENG":["Info","FAQ","Admin","Log In","Log In","Feedback","Measure My Teaching","Change Password","Log Out"],
  //       "FIN":["Tietoa","FAQ","Admin","Kirjaudu sisään","Rekisteröidy","Palaute","Mittaristo","Vaihda salasana","Kirjaudu ulos"],
  //       "component_name":"pagelayout","page_name":"index"},
  //       {"ENG":["The best way to predict the future is to create it"],
  //       "FIN":["Paras tapa ennustaa tulevaisuus on luoda se"],"component_name":"pagelayout","page_name":"landing"}]
   mapStaticData(data, selectedLanguage, languageList, ComponentListAll, ComponentListByLang) {
    for ( const pages of data) {
      const tempCompenentobj = {
        component_list: undefined,
        page_name: undefined
      };
      // console.log('************************** In for a New Page ************************************** ');
      tempCompenentobj.page_name = pages.mtee_page_name;
      tempCompenentobj.component_list = {};
      for ( const componentList of pages.mtee_page_component_list) {
        // console.log('Reading page ComponentList');
        tempCompenentobj.component_list.component_name = componentList.mtee_page_component_name;
        tempCompenentobj.component_list.language_list = {};
        for ( const itemList of componentList.mtee_page_component_item_list) {
          // console.log('Reading page component itemList');
          for ( const componentDisplay of itemList.mtee_page_component_item_display) {
            // console.log(JSON.stringify(componentDisplay));
            for ( const language of languageList) {
              // console.log(JSON.stringify(language));
              // console.log("***********************************");
              if (componentDisplay[language]) {
                ComponentListByLang.push(componentDisplay[language]);
                // console.log(JSON.stringify(ComponentListByLang));
                // console.log('++++++++++++++++++++++++++++++++++');
                // console.log(JSON.stringify(tempCompenentobj['component_list']['language_list'][language]));
                if (tempCompenentobj.component_list.language_list[language] == null) {
                  tempCompenentobj.component_list.language_list[language] = [];
                  tempCompenentobj.component_list.language_list[language].push(ComponentListByLang[0]);
                  // console.log('First time for this language ---------------> ' + JSON.stringify(language));
                } else {
                  tempCompenentobj.component_list.language_list[language].push(ComponentListByLang[0]);
                  // console.log('adding item for this language -> ' + JSON.stringify(language));
                }
                // console.log(JSON.stringify(tempCompenentobj));
                // console.log('//////////////////////////////////');
                ComponentListByLang = [];
              }
            }
          }
        }
      }
      ComponentListAll.push(tempCompenentobj);
      // console.log(JSON.stringify(ComponentListAll));
    }
   }
   clearCookies() {
    this.cookieService.set('UserId', '');
    this.router.navigate(['']);
   }
}
