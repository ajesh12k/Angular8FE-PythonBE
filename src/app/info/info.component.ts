import { Component, OnInit } from '@angular/core';
import {DataShareService} from '../data-share.service';
import {CookieService} from 'ngx-cookie-service';


@Component({
  selector: 'app-info',
  templateUrl: './info.component.html',
  styleUrls: ['./info.component.css']
})
export class InfoComponent implements OnInit {
  infoComponentItems: any = {};
  navComponentItems: any = {};
  public selectedLanguage: string;
  constructor(private data: DataShareService, private  cookieService: CookieService) { }

  ngOnInit() {
    this.data.infoPageStatic.subscribe(message => this.infoComponentItems = message);
    this.data.navigationItems.subscribe(message => this.navComponentItems = message);
    this.data.currentLanguage.subscribe(language => this.selectedLanguage = language);
    if ( this.cookieService.get('UserId') === '') {
      this.cookieService.set('UserId', '-');
    }
  }
}
