$(document).ready( function () {
    var status;
    $.ajax({
        'url' : '../api/status',
        'type' : 'GET',
        'success' : function(data) {
            setstatus(data);
        }
      });
    
    loadbutton({'id':'#listenbutton',
                'url':'../api/listen',
                'txt':'ZE\nRO',
                'initfcn': function () {
                    $('#listenres').html('');
                    },
                'okfcn': function (data) {
                    $('#listenres').html(data.data.trans);
                    },
                'kofcn': function (data) {
                    $('#listenres').html('Sorry, I am busy. Please retry in a few seconds...');
                    }
                
        });

    loadbutton({'id':'#actionbutton',
                'url':'../api/action',
                'txt':'ZE\nRO',
                'initfcn': function () {
                    $('#actionres').html('');
                    },
                'okfcn': function (data) {
                    $('#actionres').html(JSON.stringify(data,null,2));
                    },
                'kofcn': function (data) {
                    $('#actionres').html(JSON.stringify(data,null,2));
                    }
                
        });
    
    function setstatus (service) {
        togglebutton({'id':'#togglebutton',
                'url':'../api/switchzero',
                'txton':'ON',
                'txtoff':'OFF',
                'initstate': service.sb,
                'initfcn': function () {
                    },
                'okfcn': function (data) {
                    },
                'kofcn': function (data) {
                    alert('Sorry, an error has occured. Please retry in a few seconds...');
                    }
                
        });
    }

});

var current;
var count;
var paused = false;

Leap.loop({enableGestures: true, background: true}, function(frame) {
  if (paused) {
    return; // Skip this update
  }
  // Gesture object data
  if (frame.gestures.length > 0) {
    for (var i = 0; i < frame.gestures.length; i++) {
      var gesture = frame.gestures[i];
      data = null;
      try {
          if(gesture.type == "swipe") {
              //Classify swipe as either horizontal or vertical
              var isHorizontal = Math.abs(gesture.direction[0]) > Math.abs(gesture.direction[1]);
              //Classify as right-left or up-down
              if(isHorizontal){
                  if(gesture.direction[0] > 0){
                      swipeDirection = "right";
                  } else {
                      swipeDirection = "left";
                  }
              } else { //vertical
                  if(gesture.direction[1] > 0){
                      swipeDirection = "up";
                  } else {
                      swipeDirection = "down";
                  }                  
              }
              if (swipeDirection == current) {
                  count = count + 1;
              } else {
                  current = swipeDirection;
                  count = 1;
              }
           }
           if(gesture.type == "circle") {
                var clockwise = false;
                var normal = '';
                var pointableID = gesture.pointableIds[0];
                var direction = frame.pointable(pointableID).direction;
                var dotProduct = Leap.vec3.dot(direction, gesture.normal);
                if (dotProduct  >  0) clockwise = true;
                if (clockwise) {
                    normal = 'circleright';
                } else {
                    normal = 'circleleft';
                }
                if (current == normal) {
                    count = count + 1;
                } else {
                    current = normal;
                    count = 1;
                }
                
           }
       } catch (err) {
           console.log(err);
       }
       console.log(current);
       if (count>30) {
              switch (current){
                  case "up":
                      data = {'cmd' : 'play', 'arg': ''};
                      break;
                  case "down":
                      data = {'cmd' : 'pause', 'arg': ''};
                      break;
                  case "left":
                      data = {'cmd' : 'previous', 'arg': ''};
                      break;
                  case "right":
                      data = {'cmd' : 'next', 'arg': ''};
                      break;
                  case "circleleft":
                      data = {'cmd' : 'volume', 'arg': '-3'};
                      break;
                  case "circleright":
                      data = {'cmd' : 'volume', 'arg': '+3'};
                      break;
                }
       }
       if (data != null && !paused) {
          console.log('Leap command');
          paused = true;
          $.ajax({
            'url' : '../api/leap',
            'type' : 'GET',
            'data' : data,
            'complete' : function() {
                current = '';
                count = 0;
                paused = false;
            }
          })
        }
     }
  }
});





