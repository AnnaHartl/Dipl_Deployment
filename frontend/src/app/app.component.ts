import { AfterViewInit, Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { NgxCaptureService } from 'ngx-capture';
import { tap } from 'rxjs/operators';
import * as mapboxgl from 'mapbox-gl';
import { environment } from 'src/environments/environment.prod';
import { ImageUploadService } from './image-upload.service';
import { DomSanitizer } from '@angular/platform-browser';
import { GeoCodingService } from './geo-coding.service';
import { ApiService, Maps } from './api.service';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ProgressComponent } from './progress/progress.component';
import { Shape } from './models/shape';
import { GlobalService } from './global.service';
import { Coords } from './models/coords';
import Chart from 'chart.js/auto';


// https://stackblitz.com/edit/google-autocomplete?file=app%2Fapp.component.html,app%2Fapp.component.ts,app%2Fapi.service.ts
// https://stackblitz.com/edit/google-autocomplete?file=app%2Fapp.component.html

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent implements OnInit, AfterViewInit {
  testForm = new FormGroup({
    food: new FormControl('', Validators.required),
    comment: new FormControl('', Validators.required),
  });
  goNext(progress: ProgressComponent) {
    progress.next();
  }

  onStateChange(event: any) {
    console.log(event);
  }

  ngAfterViewInit() {}

  @ViewChild('search')
  public searchElementRef!: ElementRef;

  public entries = [];
  showSpinner = false
  showSecondSpinner = false;




  initAutocomplete(maps: Maps) {
    let autocomplete = new maps.places.Autocomplete(
      this.searchElementRef.nativeElement
    );
    console.log(autocomplete)
  }



  inputGeo = ''
  title = 'capture-maps';
  name = 'Angular';
  img = '';
  img_name = "cover.png";
  display: any;
  image_base_url = 'http://127.0.0.1:5000/analysedImage/';
  @ViewChild('screen', { static: true }) screen: any;
  map: mapboxgl.Map | undefined;
  style = 'mapbox://styles/mapbox/satellite-v9';
  id = 0
  latLong= [0,0]
  image_name = '';
  fields: Shape[] = [];
  actField: Shape = { color: '', coordinates: [] };
  count: number = 0;
  count_class: number = 0;
  img_crop = '';
  classifiactionResult:any;

  chartOptions = {
    title: {
      text: "Basic Column Chart in Angular"
    },
    data: [{
      type: "column",
      dataPoints: [
        { label: "Apple",  y: 10  },
        { label: "Orange", y: 15  },
        { label: "Banana", y: 25  },
        { label: "Mango",  y: 30  },
        { label: "Grape",  y: 28  }
      ]
    }]

  };

  public chart: any;


  constructor(
    private captureService: NgxCaptureService,
    private imageUploadService: ImageUploadService,
    private _sanitizer: DomSanitizer,
    private geoDataService: GeoCodingService,
    private globalService:GlobalService,
    apiService: ApiService
  ) {apiService.api.then((maps) => {
    this.initAutocomplete(maps);
  });}

  ngOnInit() {
    (mapboxgl as any).accessToken = environment.mapbox.accessToken;
    this.map = new mapboxgl.Map({
      container: 'map',
      style: this.style,
      zoom: 15,
      center: [14.2525318, 48.2680409],
      preserveDrawingBuffer: true,
    });
    // Add map controls
    //this.map.addControl(new mapboxgl.NavigationControl());
    //TODO auskommentieren
    //this.globalService.image_name = "test0.png"
    this.image_name = this.globalService.image_name;
    //this.drawCanvas()

    this.imageUploadService
      .getPolygons(
        this.globalService.image_name.substring(0, this.globalService.image_name.length - 4)
      )
      .subscribe({
        next: (res) => {
          console.log(res);
          //this.fields = res
          // console.log(res[0])
          res.forEach((element) => {
            var s = String(element).split(',');

            var cord: Coords = { x: 0, y: 0 };
            var list = [];
            for (let index = 1; index < s.length; index++) {
              const temp = s[index];

              if (index % 2 == 0) {
                cord.y = Number(temp);
                list.push(cord);
              } else {
                cord.x = Number(temp);
              }
            }

            var shape: Shape = { color: s[0], coordinates: list };
            this.fields.push(shape);
            console.log(shape);
          });
          //this.fields = res
        },
      });
  }

  makeCapture() {
    this.img_name = "cover.png"
    this.showSpinner = true
    this.captureService
      .getImage(this.screen.nativeElement, true)
      .pipe(
        tap((img) => {
          this.img = img;
          fetch(this.img)
            .then((res) => res.blob())
            .then((blob) => {
              const file = new File([blob], "test"+this.id+".png", {
                type: 'image/png',
              });
              console.log("got image")
              this.showSpinner = true

              const formData = new FormData();
              formData.append('file', file, file.name);
              console.log("sendet image zum analysieren")
              this.imageUploadService.analyseImage(formData).subscribe({
                error: (er) => {
                  this.img_name = "cover.png"
                  console.log("fehler empfangen analysieren fertig")
                  this.img_name = file.name;
                  this.globalService.image_name = file.name

                  this.showSpinner = false
                  this.id++

                  if(this.id > 2){
                    this.id = 0
                  }
                },
              });
            });
        })
      )
      .subscribe({
        next: res =>{
          console.log("capture ausgeführt")
        }
      });
  }

  findLatLong() {
    console.log(this.searchElementRef.nativeElement.value)
    console.log(this.searchElementRef)
    console.log(this.inputGeo)
    this.inputGeo = this.searchElementRef.nativeElement.value
    this.geoDataService.getLatLong(this.inputGeo).subscribe({
      next: data=>
      {
        this.latLong = data
        this.map?.setCenter([this.latLong[1], this.latLong[0]])

      },
      error: error=>{alert("ERROR")}
    })
    console.log(this.latLong)

   }

   // Hier geht classification los
   drawCanvas() {
    const canvas: any = document.getElementById('gameCanvas');
    var ctx = canvas.getContext('2d');
    ctx.canvas.width = 1300;
    ctx.canvas.height = 730;

    //Bild für die Fabauswahl
    const image: any = new Image(1300, 730);
    image.onload = function () {
      ctx.drawImage(image, 0, 0, 1300, 730);
    };
    //image.src = 'assets/field_20.png';
    //console.log(this.image_name)
    console.log(this.globalService.image_name)
    image.src = "http://127.0.0.1:5000/analysedImage/thick_"+this.globalService.image_name+ '?' + new Date().getTime();
    image.setAttribute('crossOrigin', '');

    //Click eventlistener
    canvas.addEventListener(
      'click',
      function (evt: any) {
        var mousePos = getMousePos(canvas, evt);
        const i = ctx.getImageData(mousePos.x, mousePos.y, 600, 600).data;
        //console.log('#' +((1 << 24) + (i[0] << 16) + (i[1] << 8) + i[2]).toString(16).slice(1));
        var colorBox = document.getElementById('colorBox');
        colorBox!.style.backgroundColor =
          '#' +
          ((1 << 24) + (i[0] << 16) + (i[1] << 8) + i[2]).toString(16).slice(1);
      },
      false
    );

    //Mausposition
    function getMousePos(canvas: any, evt: any) {
      var rect = canvas.getBoundingClientRect();
      return {
        x: evt.clientX - rect.left,
        y: evt.clientY - rect.top,
      };
    }
  }

  fieldClicked(field: Shape) {
    console.log('clicked');
    this.actField = field;
  }

  analyseField() {
    var colorBox = document.getElementById('colorBox');
    console.log(colorBox!.style.backgroundColor.split(','))
    var strings = colorBox!.style.backgroundColor.split(',')
    var red = Number(strings[0].replace( /^\D+/g, ''))
    var green = Number(strings[1].replace( /^\D+/g, ''))
    var blue = Number(strings[2].match(/\d/g)!.join(""))

    var hex = ((1 << 24) + (red << 16) + (green << 8) + blue).toString(16).slice(1);
    console.log(hex)


    console.log(this.globalService.image_name.substring(0, this.globalService.image_name.length - 4))
    this.imageUploadService
      .crop_image(
        this.globalService.image_name.substring(0, this.globalService.image_name.length - 4),
        hex,
        this.count
      )
      .subscribe();
    this.count += 1;

    if (this.count >= 3) this.count = 0;

    this.getAnalysedField();
  }

  // Hiere geth Analyse los
  getAnalysedField() {
    this.showSecondSpinner = true;
    const image: any = new Image(600, 600);
    console.log("test")
    this.img_crop = "http://127.0.0.1:5000/analysedField/crop_"+this.globalService.image_name.substring(0, this.globalService.image_name.length - 4) +"/" +this.count;
    //this.classifiactionResult = "http://127.0.0.1:5000/getJsonColors/crop_"+this.globalService.image_name.substring(0, this.globalService.image_name.length - 4);
    //console.log("!!!" + this.classifiactionResult)
    console.log(this.img_crop);
    image.setAttribute('crossOrigin', '');

    this.imageUploadService
      .getJsonClassifiaction(
        "crop_" + this.globalService.image_name.substring(0, this.globalService.image_name.length - 4)
      )
      .subscribe({
        next: data=>
        {
          this.showSecondSpinner = false;

          this.classifiactionResult = data
          console.log(this.classifiactionResult)
          var splitted = this.classifiactionResult.split(";",3);
          console.log(splitted)

          this.chart = new Chart("MyChart", {
            type: 'bar', //this denotes tha type of chart
            data: {// values on X-Axis
              labels: ['Dauerweide', 'Raps', 'Wein'],
               datasets: [
                {
                  label: "",
                  data: [Number(splitted[0])*100,Number(splitted[1])*100, Number(splitted[2])*100],
                  backgroundColor: ["rgb(51,92,103)", "rgb(38,87,45)", "rgb(179,27,67)"]
                }
              ]
            },
            options: {
              aspectRatio:2.5,
              scales: {
                y: {
                    suggestedMin: 0,
                    suggestedMax: 100
                }
            },

          }

          });

        }
      })






  }


}

