import { Component, OnInit, ViewChild } from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {WebserviceCallerService} from '../webservice-caller.service';
import {ActivatedRoute, Router} from '@angular/router';
import {DataShareService} from '../data-share.service';
import {CookieService} from 'ngx-cookie-service';
import {ShowMessageService} from '../show-message.service';
import {MatSnackBar} from '@angular/material/snack-bar';
import {MatAccordion} from '@angular/material/expansion';
import {MatDatepicker, MatDatepickerInputEvent} from '@angular/material/datepicker';

@Component({
  selector: 'app-campaign',
  templateUrl: './campaign.component.html',
  styleUrls: ['./campaign.component.css']
})
export class CampaignComponent implements OnInit {
  @ViewChild (MatAccordion) accordion: MatAccordion;
  // define page forms here
  createCampaignForm: FormGroup;
  searchCampaignForm: FormGroup;
  // define show message variables here
  errorMsg: any = {};
  successMsg: any = {};
  minDate: Date;
  maxDate: Date;
  startDate =  new Date();
  endDate = new Date();
  panelOpenState = false;
  // define api request structures here
  public searchRequest = {
    mtee_campaign_code: undefined,
  };
  public createCampaignCodeRequest = {
    mtee_campaign_code: undefined,
    mtee_campaign_type: undefined,
    mtee_campaign_description: undefined,
    mtee_campaign_start_date: undefined,
    mtee_campaign_end_date: undefined,
    mtee_user_id: undefined
  };
  public searchCampaignCodeRequest = {
    mtee_campaign_code: undefined,
    mtee_campaign_type: undefined,
    mtee_campaign_description: undefined,
    mtee_campaign_start_date: undefined,
    mtee_campaign_end_date: undefined,
    mtee_user_id: undefined
  };
  // define component specific variables here
  userLoginDetails: any = {};
  public selectedLanguage: string;
  //
  constructor(public rest: WebserviceCallerService,
              private route: ActivatedRoute,
              private router: Router,
              private dataBus: DataShareService,
              private formBuilder: FormBuilder,
              public cookieService: CookieService,
              public showMessageService: ShowMessageService,
              public snackBar: MatSnackBar) {
               // Set the minimum to today and December 31st a year in the future.
               const currentYear = new Date().getFullYear();
               this.minDate = new Date();
               this.maxDate = new Date(currentYear + 1, 11, 31);
               }
  // ********************************************************************************
  ngOnInit(): void {
  this.dataBus.currentLanguage.subscribe(language => this.selectedLanguage = language);
  this.dataBus.userLoginResult.subscribe(message => this.userLoginDetails = message);
  this.createCampaignForm = this.formBuilder.group({
      mtee_campaign_code: [null, Validators.compose([Validators.required, Validators.minLength(2), Validators.maxLength(8)])],
      mtee_campaign_type: [null, Validators.compose([Validators.required, Validators.minLength(3), Validators.maxLength(30)])],
      mtee_campaign_description: [null, Validators.compose([Validators.required, Validators.minLength(2), Validators.maxLength(30)])]
    });
  this.searchCampaignForm = this.formBuilder.group({
      mtee_campaign_code_search: [null, Validators.compose([Validators.minLength(2), Validators.maxLength(8)])],
      mtee_campaign_type_search: [null, Validators.compose([Validators.minLength(3), Validators.maxLength(30)])],
      mtee_campaign_description_search: [null, Validators.compose([Validators.minLength(2), Validators.maxLength(30)])]
  });
  }
  //
  //
  selectedStartDate(event: MatDatepickerInputEvent<Date>) {
    this.startDate = new Date(event.value);
    this.endDate.setHours(0, 0, 0 );
    console.log('---------------- : ' + this.startDate);
    this.createCampaignCodeRequest.mtee_campaign_start_date = this.startDate;
  }
  //
  selectedEndDate(event: MatDatepickerInputEvent<Date>) {
    this.endDate = new Date(event.value);
    this.endDate.setHours(23, 59, 59 );
    console.log('---------------- : ' + this.endDate);
    this.createCampaignCodeRequest.mtee_campaign_end_date = this.endDate;
  }
  //
  //
  selectedStartDateSearch(event: MatDatepickerInputEvent<Date>) {
    this.startDate = new Date(event.value);
    this.endDate.setHours(0, 0, 0 );
    console.log('---------------- : ' + this.startDate);
    this.searchCampaignCodeRequest.mtee_campaign_start_date = this.startDate;
  }
  //
  selectedEndDateSearch(event: MatDatepickerInputEvent<Date>) {
    this.endDate = new Date(event.value);
    this.endDate.setHours(23, 59, 59 );
    console.log('---------------- : ' + this.endDate);
    this.searchCampaignCodeRequest.mtee_campaign_end_date = this.endDate;
  }
  //
  //
  createcampaign () {
        // console.log(' Inside createcampaign ');
        this.createCampaignCodeRequest.mtee_campaign_code = this.createCampaignForm.value.mtee_campaign_code;
        this.createCampaignCodeRequest.mtee_campaign_type = this.createCampaignForm.value.mtee_campaign_type;
        this.createCampaignCodeRequest.mtee_campaign_description = this.createCampaignForm.value.mtee_campaign_description;
        this.createCampaignCodeRequest.mtee_user_id = this.userLoginDetails;
        console.log(this.createCampaignCodeRequest);
        this.rest.createCampaign(this.createCampaignCodeRequest)
            .subscribe(data => {
              if ( data.status === 'success') {
                this.snackBar.open(data.result, '', {
                  verticalPosition: 'bottom', horizontalPosition: 'center', panelClass: ['successSnackbar'], duration : 3000
                });
              } else {
                this.snackBar.open(data.result, '', {
                  verticalPosition: 'bottom', horizontalPosition: 'center', panelClass: ['errorSnackbar'], duration : 3000
                });
              }
            });
  }
  //
  searchcampaign () {
        console.log(' Inside editcampaign ');
        this.searchCampaignCodeRequest.mtee_campaign_code = this.searchCampaignForm.value.mtee_campaign_code;
        this.searchCampaignCodeRequest.mtee_campaign_type = this.searchCampaignForm.value.mtee_campaign_type;
        this.searchCampaignCodeRequest.mtee_campaign_description = this.searchCampaignForm.value.mtee_campaign_description;
        console.log(this.searchCampaignCodeRequest);
        this.rest.searchCampaign(this.searchCampaignCodeRequest)
            .subscribe(data => {
              if ( data.status === 'success') {
                this.snackBar.open(data.result, '', {
                  verticalPosition: 'bottom', horizontalPosition: 'center', panelClass: ['successSnackbar'], duration : 3000
                });
              } else {
                this.snackBar.open(data.result, '', {
                  verticalPosition: 'bottom', horizontalPosition: 'center', panelClass: ['errorSnackbar'], duration : 3000
                });
              }
            });
  }

}
