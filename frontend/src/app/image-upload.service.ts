import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';


@Injectable({
  providedIn: 'root'
})
export class ImageUploadService {


  constructor(private http: HttpClient) { }

  analyseImage(formData:FormData) {
    return this.http.post('http://127.0.0.1:5000/analyse_image', formData)
  }
  getPolygons(imagename: string) {
    return this.http.get<Array<string>>('http://127.0.0.1:5000/polygons/'+imagename)
  }
  crop_image(image_name: string, color:string, count:number) {
    return this.http.get("http://127.0.0.1:5000/crop_image/"+image_name+"/"+color+"/"+count)
  }
  getJsonClassifiaction(imagename: string) {
    return this.http.get('http://127.0.0.1:5000/json_classification/'+ imagename);

  }

}
