import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';


@Injectable({
  providedIn: 'root'
})
export class GeoCodingService {


  constructor(private http: HttpClient) { }

  getLatLong(geodata: string) {
    return this.http.get<number[]>('http://127.0.0.1:5000/get_lat_long/'+ geodata)
  }

}
