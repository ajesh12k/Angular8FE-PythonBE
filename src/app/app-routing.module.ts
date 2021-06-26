import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { RouterModule, Routes } from '@angular/router';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HomeComponent } from './home/home.component';
import {QuestionsComponent} from './questions/questions.component';
import {FeedbackComponent} from './feedback/feedback.component';
import { LogInComponent } from './log-in/log-in.component';
import { LogoutComponent } from './logout/logout.component';
import { SettingsComponent } from './settings/settings.component';
import {InfoComponent} from './info/info.component';
import {FaqComponent} from './faq/faq.component';
import {ForgetpasswordComponent} from './forgetpassword/forgetpassword.component';
import { ResetpasswordComponent} from './resetpassword/resetpassword.component';
import {ReportComponent} from './report/report.component';
import {LocationComponent} from './location/location.component';
import {CampaignComponent} from './campaign/campaign.component';
import { SignupComponent } from './signup/signup.component';
const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'login', component: LogInComponent },
  { path: 'register', component: SignupComponent },
  { path: 'logout', component: LogoutComponent },
  { path: 'questions', component: QuestionsComponent },
  { path: 'feedback', component: FeedbackComponent },
  { path: 'settings', component: SettingsComponent },
  { path: 'info', component: InfoComponent },
  { path: 'faq', component: FaqComponent },
  { path: 'forgetpassword', component: ForgetpasswordComponent },
  { path: 'resetPassword', component: ResetpasswordComponent },
  { path: 'municipalityChange', component: LocationComponent },
  { path: 'campaign', component: CampaignComponent },
  { path: 'reportByDate', component: ReportComponent }
];

@NgModule({
  imports: [
  RouterModule.forRoot(routes),
  FormsModule,
  HttpClientModule],
  exports: [RouterModule]
})
export class AppRoutingModule { }
