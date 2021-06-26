import { Component, OnInit } from '@angular/core';
import {DataShareService} from '../data-share.service';
import {CookieService} from 'ngx-cookie-service';


@Component({
  selector: 'app-faq',
  templateUrl: './faq.component.html',
  styleUrls: ['./faq.component.css']
})
export class FaqComponent implements OnInit {
  faqComponentItems: any = {};
  navComponentItems: any = {};
  public selectedLanguage: string;
  constructor(private data: DataShareService, private  cookieService: CookieService) { }

  ngOnInit() {
    this.data.faqPageStatic.subscribe(message => this.faqComponentItems = message);
    this.data.navigationItems.subscribe(message => this.navComponentItems = message);
    this.data.currentLanguage.subscribe(language => this.selectedLanguage = language);
    if ( this.cookieService.get('UserId') === '') {
      this.cookieService.set('UserId', '-');
    }
  }
}
