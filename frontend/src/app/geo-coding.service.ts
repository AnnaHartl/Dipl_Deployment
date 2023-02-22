import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from 'src/environments/environment.prod';


@Injectable({
  providedIn: 'root'
})
export class GeoCodingService {


  constructor(private http: HttpClient) { }

  getLatLong(geodata: string) {
    return this.http.get<number[]>(environment.host+'/get_lat_long/'+ geodata)
  }

}
