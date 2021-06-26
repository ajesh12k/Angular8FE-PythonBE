import { BrowserModule } from '@angular/platform-browser';
import { NgModule , CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { RouterModule, Routes } from '@angular/router';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FlexLayoutModule } from '@angular/flex-layout';
import { CookieService} from 'ngx-cookie-service';
import { MatBadgeModule } from '@angular/material/badge';
import { MatButtonModule } from '@angular/material/button';
import { MatButtonToggleModule } from '@angular/material/button-toggle';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatDialogModule } from '@angular/material/dialog';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatIconModule } from '@angular/material/icon';
import { MatListModule } from '@angular/material/list';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatRadioModule } from '@angular/material/radio';
import { MatSelectModule } from '@angular/material/select';
import {MatDatepickerModule, MatDatepicker} from '@angular/material/datepicker';
import { FormlyModule } from '@ngx-formly/core';
import { FormlyBootstrapModule } from '@ngx-formly/bootstrap';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { ServiceWorkerModule } from '@angular/service-worker';
import { environment } from '../environments/environment';
import { LogService } from './logger.service';
import { WebserviceCallerService } from './webservice-caller.service';
import { DataShareService } from './data-share.service';
import { QuestionsComponent } from './questions/questions.component';
import { FeedbackComponent } from './feedback/feedback.component';
import { LoginhelpersModule } from './loginhelpers/loginhelpers.module';
import { LogInComponent } from './log-in/log-in.component';
import { LogoutComponent } from './logout/logout.component';
import { SettingsComponent } from './settings/settings.component';
import { InfoComponent } from './info/info.component';
import { FaqComponent } from './faq/faq.component';
import { ForgetpasswordComponent } from './forgetpassword/forgetpassword.component';
import { ReportComponent } from './report/report.component';
import { MatPasswordStrengthModule } from '@angular-material-extensions/password-strength';
import { SignupComponent } from './signup/signup.component';
import { ResetpasswordComponent } from './resetpassword/resetpassword.component';
import {ShowMessageService} from './show-message.service';
import {MatNativeDateModule} from "@angular/material/core";
import { LocationComponent } from './location/location.component';
import { CampaignComponent } from './campaign/campaign.component';


@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    QuestionsComponent,
    FeedbackComponent,
    LogInComponent,
    LogoutComponent,
    SettingsComponent,
    InfoComponent,
    FaqComponent,
    ForgetpasswordComponent,
    ReportComponent,
    SignupComponent,
    ResetpasswordComponent,
    LocationComponent,
    CampaignComponent,
  ],
    imports: [
        BrowserModule,
        HttpClientModule,
        BrowserAnimationsModule,
        FlexLayoutModule,
        FormsModule,
        ReactiveFormsModule,
        MatDatepickerModule,
        MatNativeDateModule,
        MatIconModule,
        MatButtonModule,
        MatSelectModule,
        AppRoutingModule,
        ServiceWorkerModule.register('ngsw-worker.js', {enabled: environment.production}),
        FormlyBootstrapModule,
        FormlyModule.forRoot({
            validationMessages: [
                {name: 'required', message: 'This field is required'},
            ],
        }),
        MatRadioModule,
        LoginhelpersModule,
        MatPasswordStrengthModule.forRoot()
    ],
  providers: [
    LogService,
    WebserviceCallerService,
    ShowMessageService,
    DataShareService,
    CookieService,
  ],
  bootstrap: [AppComponent],
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class AppModule { }
