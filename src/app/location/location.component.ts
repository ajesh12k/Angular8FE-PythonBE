import { Component, OnInit, ViewChild } from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {WebserviceCallerService} from '../webservice-caller.service';
import {ActivatedRoute, Router} from '@angular/router';
import {DataShareService} from '../data-share.service';
import {CookieService} from 'ngx-cookie-service';
import {ShowMessageService} from '../show-message.service';
import {MatSnackBar} from '@angular/material/snack-bar';
import {MatAccordion} from '@angular/material/expansion';

// define page interfaces here

interface MunicipalityInterface {
  name_municipality_1: string;
  name_municipality_2: string;
  code_municipality: number;
  name_provience_1: string;
  name_provience_2: string;
  code_provience: number;
}

// page components
@Component({
  selector: 'app-location',
  templateUrl: './location.component.html',
  styleUrls: ['./location.component.css']
})

export class LocationComponent implements OnInit {
  @ViewChild (MatAccordion) accordion: MatAccordion;
  // define page forms here
  formSearchByCodeMun: FormGroup;
  formSearchByCodePro: FormGroup;
  formUpdateMunicipalityDetails: FormGroup;
  formSearchByNameMun: FormGroup;
  // formSearchByNamePro: FormGroup;
  // define show message variables here
  errorMsg: any = {};
  successMsg: any = {};
  // define api request structures here
  public searchRequest = {
    mtee_municipality_code: undefined,
  };
  public updateMunicipalityDetailsRequest = {
    mtee_municipality_code_new: undefined,
    mtee_municipality_name_1_new: undefined,
    mtee_municipality_name_2_new: undefined,
    mtee_municipality_code: undefined,
    mtee_municipality_name_1: undefined,
    mtee_municipality_name_2: undefined,
    mtee_user_id: undefined,
    change_municipality: true,
    change_province: false
  };
  public deleteMunicipalityDetailsRequest = {
    mtee_municipality_code: undefined,
    mtee_user_id: undefined
  };
  // define api response structure here
  public searchResult: any;
  // define conditional page element control variables here
  found: boolean;
  editForm: boolean;
  panelOpenState = false;
  // define component specific variables here
  userLoginDetails: any = {};
  public selectedLanguage: string;
  municipalities1: any = [];
  municipalities2: any = [];
  selectedMunicipality1: MunicipalityInterface;
  selectedMunicipality2: MunicipalityInterface;
  municipalityList1: any = {};
  municipalityList2: any = {};
  municipalityListShow1: any = [];
  municipalityListShow2: any = [];
  selectedMunicipalityToSave: any = [];
  provienceList: any = [];
  provienceRecord: any = [];
  selectedProvience: any;
  //
  constructor(public rest: WebserviceCallerService,
              private route: ActivatedRoute,
              private router: Router,
              private dataBus: DataShareService,
              private formBuilder: FormBuilder,
              public cookieService: CookieService,
              public showMessageService: ShowMessageService,
              public snackBar: MatSnackBar) {
  }
  //
  //
  ngOnInit() {
    // console.log(this.loginComponentItems);
    this.dataBus.currentLanguage.subscribe(language => this.selectedLanguage = language);
    this.dataBus.userLoginResult.subscribe(message => this.userLoginDetails = message);
    this.found = false;
    this.editForm = false;
    this.formSearchByCodeMun = this.formBuilder.group({
      mtee_municipality_code: [null, Validators.compose([Validators.required, Validators.minLength(2), Validators.maxLength(8)])],
    });
    this.formSearchByCodePro = this.formBuilder.group({
      mtee_province_code: [null, Validators.compose([Validators.required, Validators.minLength(2), Validators.maxLength(8)])],
    });
    this.formSearchByNameMun = this.formBuilder.group({
      mtee_municipality_name: [null, Validators.compose([Validators.required, Validators.minLength(2), Validators.maxLength(8)])],
    });
    this.formUpdateMunicipalityDetails = this.formBuilder.group({
      mtee_municipality_code_new: [null, Validators.compose([Validators.required, Validators.minLength(3), Validators.maxLength(8)])],
      mtee_municipality_name_1_new: [null, Validators.compose([Validators.required, Validators.minLength(2), Validators.maxLength(30)])],
      mtee_municipality_name_2_new: [null, Validators.compose([Validators.required, Validators.minLength(2), Validators.maxLength(30)])]
    });
    this.getProvienceList();
    this.getMunicipalityList();
  }
  //
  searchMunicipalityByCode() {
    // console.log('Searching Municipality');
    this.found = false;
    this.searchRequest.mtee_municipality_code = this.formSearchByCodeMun.value.mtee_municipality_code;
    this.rest.searchByMunicipalityCode(this.searchRequest)
            .subscribe(data => {
              if ( data.status === 'success') {
                if(data.result.length !== 0) {
                this.searchResult = data.result[0];
                this.found = true;
                this.editForm = false;
                this.updateMunicipalityDetailsRequest.mtee_municipality_code = this.searchResult.mtee_municipality_code;
                this.updateMunicipalityDetailsRequest.mtee_municipality_name_1 = this.searchResult.mtee_municipality_name_1;
                this.updateMunicipalityDetailsRequest.mtee_municipality_name_2 = this.searchResult.mtee_municipality_name_2;
                this.snackBar.open('Result Found! You can now edit details.', '', {
                  verticalPosition: 'bottom', horizontalPosition: 'center', panelClass: ['successSnackbar'], duration : 6000
                });
                }else {
                this.searchResult.mtee_municipality_code = '';
                this.searchResult.mtee_municipality_name_1 = '';
                this.searchResult.mtee_municipality_name_2 = '';
                this.snackBar.open('No result Found. You can create new record', '', {
                  verticalPosition: 'bottom', horizontalPosition: 'center', panelClass: ['errorSnackbar'], duration : 7000
                });
                this.found = true;
                // console.log(data);
                this.updateMunicipalityDetailsRequest.mtee_municipality_code = this.formSearchByCodeMun.value.mtee_municipality_code;
                this.updateMunicipalityDetailsRequest.mtee_municipality_name_1 = ' ';
                this.updateMunicipalityDetailsRequest.mtee_municipality_name_2 = ' ';
                }
              }
            });
  }
  //
  searchMunicipalityByName() {
  }
  //
  clickedEdit() {
  this.updateMunicipalityDetailsRequest.mtee_municipality_code_new = ' ';
  this.updateMunicipalityDetailsRequest.mtee_municipality_name_1_new = ' ';
  this.updateMunicipalityDetailsRequest.mtee_municipality_name_2_new = ' ';
  this.editForm = true;
  this.snackBar.open('fill details correctly.', '', {
                  verticalPosition: 'bottom', horizontalPosition: 'center', panelClass: ['successSnackbar'], duration : 3000
                });
  }
  //
  clickedDelete() {
   this.deleteMunicipalityDetailsRequest.mtee_municipality_code = this.searchResult.mtee_municipality_code;
   // console.log(this.deleteMunicipalityDetailsRequest);
   this.deleteMunicipalityDetailsRequest.mtee_user_id = localStorage.getItem('UserId');
   this.snackBar.open('The selected municipality will be deleted.', '', {
                  verticalPosition: 'bottom', horizontalPosition: 'center', panelClass: ['successSnackbar'], duration : 3000
   });
   this.rest.deleteLocationDetails(this.deleteMunicipalityDetailsRequest)
   .subscribe(data => {
              if ( data.status === 'success') {
                  this.snackBar.open('Municipality Deleted!', '', { verticalPosition: 'bottom', horizontalPosition: 'center', panelClass: ['successSnackbar'], duration : 6000 });
              } else {
                this.snackBar.open('Failed to delete the selected municipality, Try later', '', { verticalPosition: 'bottom', horizontalPosition: 'center', panelClass: ['errorSnackbar'], duration : 7000});
              }
              this.found = false;
              this.searchResult.mtee_municipality_code = '';
              this.searchResult.mtee_municipality_name_1 = '';
              this.searchResult.mtee_municipality_name_2 = '';
              });
  }
  //
  //
  updateMunicipalityDetails() {
    // console.log('Inside updateMunicipalityDetails');
    // this.editForm = false;
    this.updateMunicipalityDetailsRequest.mtee_municipality_code_new = this.formUpdateMunicipalityDetails.value.mtee_municipality_code_new;
    this.updateMunicipalityDetailsRequest.mtee_municipality_name_1_new = this.formUpdateMunicipalityDetails.value.mtee_municipality_name_1_new;
    this.updateMunicipalityDetailsRequest.mtee_municipality_name_2_new = this.formUpdateMunicipalityDetails.value.mtee_municipality_name_2_new;
    this.updateMunicipalityDetailsRequest.mtee_user_id = localStorage.getItem('UserId');
    this.rest.updateLocationDetails(this.updateMunicipalityDetailsRequest)
            .subscribe(data => {
              if ( data.status === 'success') {
              this.snackBar.open('Changes Saved!', '', {
                  verticalPosition: 'bottom', horizontalPosition: 'center', panelClass: ['successSnackbar'], duration : 6000
                });
                // console.log(data);
                this.searchResult = data.result[0];
                this.found = true;
                // console.log(this.searchResult);
              }
            });
  }
  //
  //
  getProvienceList() {
    this.rest.getProvienceList().subscribe(
      (data: {}) => {
        this.provienceRecord = data;
        // console.log('Province data: ');
        // console.log(data);
        // tslint:disable-next-line:forin
        for (const x in data) {
          this.provienceList.push(data[x]);
        }
      }
    );
  }
  //
  //
  onProvienceSelect(provience) {
    this.selectedProvience = provience.value;
    this.municipalityListShow1 = [];
    // tslint:disable-next-line:forin
    for (const x in this.municipalities1) {
      const listedProvience = this.municipalities1[x].name_2;
      if (listedProvience === this.selectedProvience) {
        // console.log('Provience matched');
        this.municipalityListShow1.push(this.municipalities1[x].name_1);
      }
    }
    // console.log(this.municipalityListShow1);
    // console.log('Provience Value Sent');
    // console.log(this.selectedProvience);
  }
  //
  searchProvinceByCode() {
  console.log('Inside searchProvinceByCode ');
  }
  //
  getMunicipalityList() {
  // console.log('Inside getMunicipalityList in question component caller');
  this.municipalityList1 = {};
  this.rest.getMunicipalityList().subscribe(data => {
  if (data) {
     this.searchResult = data;
     const temp1: MunicipalityInterface = {
                name_municipality_1: undefined,
                name_municipality_2: undefined,
                code_municipality: undefined,
                name_provience_1: undefined,
                code_provience: undefined,
                name_provience_2: undefined
     };
     for (const x in this.searchResult) {
          temp1.name_municipality_1 = this.searchResult[x].mtee_municipality_name_1;
          temp1.name_municipality_2 = this.searchResult[x].mtee_municipality_name_2;
          temp1.code_municipality = this.searchResult[x].mtee_municipality_code;
          temp1.name_provience_1 = this.searchResult[x].mtee_county_provience_name_1;
          temp1.name_provience_2 = this.searchResult[x].mtee_county_provience_name_2;
          temp1.code_provience = this.searchResult[x].mtee_county_provience_code;
          this.municipalities1.push(temp1);
          this.municipalityListShow1.push(data[x].mtee_municipality_name_1);
     }
     this.municipalities1.sort((a1, b1) => a1.name_municipality_1.localeCompare(b1.name_municipality_1));
     this.municipalityListShow1.sort((a1, b1) => a1.localeCompare(b1));
     // console.log(this.municipalities1);
  }
  });
  }
  //
  // On municpilatySelect
  onMunicipalitySelect(municipality) {
  // console.log('---- municipality --: ', municipality.value);
  this.selectedMunicipalityToSave = municipality.value;
  }
  //

}
