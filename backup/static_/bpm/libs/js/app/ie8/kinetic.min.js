var Kinetic = {
     methods:{
               el:window,
               queue:[],
               setWidth:function(w){
                         var  dzc =  $('[data-zoomcontent]');
                              dzc.width(w);
                         return this.el.width(w);
               },
               getWidth:function(){
                    return this.el.width();
               },
               setHeight:function(h){
                    var  dzc =  $('[data-zoomcontent]');
                         dzc.height(h);
                    return this.el.height(h);
               },
               getHeight:function(){
                    return this.el.height();
               },
               add:function(obj){
                    return this.queue.push($(obj.el));
               },
               draw:function(){
                    for (var i = 0; i < this.queue.length; i++) {
                         this.el.append(this.queue[i]);
                    }
               },
               setDraggable:function(){
                    if(PublishWebAttributes.ie8.draggable){
                         Kinetic.canvas.draggable({
                              drag: function( event, ui ) {
                                   var limits = {};

                                 if(ui.position.left >= 0){
                                     ui.position.left = 0;
                                   }

                                 if(ui.position.top >= 0){
                                     ui.position.top = 0;
                                   }

                                   var imgW = ui.helper.find('img').width();
                                   var imgH = ui.helper.find('img').height();

                                   var helperW = ui.helper.width();
                                   var helperH = ui.helper.parents('.data-zoomcontainer').height();

                                   if(imgW > helperW ){
                                        limits.x = (imgW - helperW) * -1;
                                   }else{
                                        limits.x = 0;
                                   }

                                   if(imgH > helperH){
                                        limits.y = (imgH - helperH) * -1;
                                   }else{
                                        limits.y = 0;
                                   }

                                   if(ui.position.top < limits.y){
                                     ui.position.top = limits.y;
                                   }

                                   if(ui.position.left < limits.x){
                                     ui.position.left = limits.x;
                                   }
                              }
                         });
                    }else{
                         $('[data-zoompanepanel]').hide();
                         $('[data-zoomiconpanepanel]').hide();
                    }
               },
               getScale:function(){
                    return {x:1, y:1};
               },
               setPosition:function(x,y){
                    this.setX(x);
                    this.setY(y);
               },
               setX:function(x){
                    this.el.css('left', x);
               },
               getX:function(){

                    var pos = this.el.position();
                    var rValue = (pos)? pos.left: 0;

                    return rValue;
               },
               setY:function(y){
                    this.el.css('top', y);
               },
               getY:function(){
                   var pos = this.el.position();
                    var rValue = (pos)? pos.top: 0;

                    return rValue;
               },
               on:function(ev, exe){
                    this.el.on(ev, exe);
               },
               remove:function(){
                    this.el.remove();
                    Kinetic.canvas.empty();
               },
               removeClass:function(cl){

               }
     },
     Stage: function(op){
          var canvas = Kinetic.canvas = $('<div class="canvas kineticjs-content"></div>');
          Kinetic.canvas.empty();

          var container = $('#'+op.container);
          container.append(canvas);

          var stageObject = $.extend(true, {},Kinetic.methods);
               stageObject.el = Kinetic.canvas;

          $('[data-zoomcontrol]').remove();

          return stageObject;
     },
     Layer: function(){
          var layer = $('<div class="layer"></div>');

          var layerObject = $.extend(true, {},Kinetic.methods);
               layerObject.el = layer;

          return layerObject;
     },
     Image: function(op){
          var image = $('<img src="'+op.image.src+'"/>');

          Kinetic.canvas.append(image);

          var imgObject = $.extend(true, {},Kinetic.methods);
               imgObject.el = image;

          image.on('load',function(){
               var _self = $(this);

               var dzc =  $('[data-zoomcontent]');
               var kc = Kinetic.canvas;

               dzc.width(kc.width());
               dzc.height(kc.height());

               dzc.addClass('ui-scrolleable');

               $('.zoom-application-container').addClass('ui-normal-cursor');

               _self.addClass('ui-real-data');
               kc.width(_self.width());
               kc.height(_self.height());
          });

          return imgObject;
     },
     Animation:function(){
          return {};
     }
};