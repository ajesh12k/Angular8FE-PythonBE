import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {WebserviceCallerService} from '../webservice-caller.service';
import {ActivatedRoute, Router} from '@angular/router';
import {DataShareService} from '../data-share.service';
import {CookieService} from 'ngx-cookie-service';

@Component({
  selector: 'app-feedback',
  templateUrl: './feedback.component.html',
  styleUrls: ['./feedback.component.css']
})
export class FeedbackComponent implements OnInit {

public selectedCategory = null;



  feedbackComponentItems: any = {};
  public userLoginDetails: any = {};
  public selectedLanguage: string;
  public listFeedbackParameter: any = [];
  public listUserResponseDate: any = [];
  public listUserResponseDateFormated: any = [];
  public listUserResponses: any = [];
  public userRequestBody = {
    username: undefined
  };
  public userRequestDate = {
    selectedDate: undefined
  };
  errorMsg: any = {};
  successMsg: any = {};
  //
  constructor(public rest: WebserviceCallerService,
              private route: ActivatedRoute,
              private router: Router,
              private dataBus: DataShareService,
              public cookieService: CookieService) { }

  ngOnInit() {
    this.dataBus.userLoginResult.subscribe(message => this.userLoginDetails = message);
    console.log(this.userLoginDetails.mtee_user_id);
    this.userRequestBody.username = this.userLoginDetails.mtee_user_id;
    this.dataBus.feedbackPageStatic.subscribe(message => this.feedbackComponentItems = message);
    this.dataBus.currentLanguage.subscribe(language => this.selectedLanguage = language);
    this.getFeedbackParameters();
    this.getAllDatesForUser();
    this.cookieService.set('showFeedback', 'N', undefined, '/', undefined, false);
    // console.log(this.selectedLanguage);
    // console.log(this.feedbackComponentItems);
  }
    changeCategory(newCategory?: string) {
        this.selectedCategory = newCategory;
    }

  //
  getFeedbackParameters() {
    // console.log('Inside getFeedbackParameters in feedback component caller');
    this.listFeedbackParameter = [];
    this.rest.getFeedbackParameters().subscribe
    ((data: {
        result: any;
      }) => {
        console.log('logging feedback parameter list content');
        this.listFeedbackParameter = data.result;
        console.log(this.listFeedbackParameter);
      }
    );
  }
  //
  getAllDatesForUser() {
    console.log('Inside getAllDatesForUser in feedback component caller');
    this.listUserResponseDate = [];
    this.rest.getAllDatesForUser(this.userRequestBody).subscribe
    ((data: { result: any; }) => {
        console.log('logging response dates for user');
        this.listUserResponseDate = data.result;
        console.log(this.listUserResponseDate);
        this.userRequestDate.selectedDate = this.listUserResponseDate[0];
        this.getAllResponseOfUser();
      }
    );
  }
  //
  getAllResponseOfUser() {
    // console.log('Inside getAllResponseOfUser in feedback component caller');
    this.listUserResponses = [];
    this.rest.getAllResponseOfUser(this.userRequestBody, this.userRequestDate).subscribe
    ((data: {
        result: any;
      }) => {
        console.log('logging all responses for user');
        this.listUserResponses = data.result;
        console.log(this.listUserResponses);
      }
    );
  }
  //
  selectedDate($event: any, userDate: any ) {
    console.log('Date Selected');
    console.log(userDate);
    this.userRequestDate.selectedDate = userDate;
    this.getAllResponseOfUser();
  }
  //
  goToSpecificUrl(url): void {
    window.location.href = url;
  }



}
