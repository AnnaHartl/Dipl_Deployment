import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment.prod';


@Injectable({
  providedIn: 'root'
})
export class ImageUploadService {


  constructor(private http: HttpClient) { }

  analyseImage(formData:FormData) {
    return this.http.post(environment.host+'/analyse_image', formData)
  }
  getPolygons(imagename: string) {
    return this.http.get<Array<string>>(environment.host+'/polygons/'+imagename)
  }
  crop_image(image_name: string, color:string, count:number) {
    return this.http.get(environment.host+"/crop_image/"+image_name+"/"+color+"/"+count)
  }
  getJsonClassifiaction(imagename: string) {
    return this.http.get(environment.host+'/json_classification/'+ imagename);

  }

}
