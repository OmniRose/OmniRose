jQuery(function ($) {
  console.log('starting');


  var $compass_video_container = $("#compass_video_container");
  var $shadow_video_container  = $("#shadow_video_container");


  function setup_video_in_container($video_container) {
    var $input = $video_container.find("input");
    var video = $video_container.find("video")[0];
    var $video_current_time = $video_container.find(".current_time");
    var $play_button  = $video_container.find(".play_button");
    var $step_buttons = $video_container.find(".step_button");

    $input.on('change', function (event) {
      var file = this.files[0];
      console.debug(file, file.type);

      // check that we can play this sort of file
      if (video.canPlayType(file.type)) {
        console.log('can play video');
        var fileURL = URL.createObjectURL(file);
        video.src = fileURL;

        $video_current_time.text("0");

        $(video).on('timeupdate', function () {
          $video_current_time.text(video.currentTime);
        });

        $input.hide();
      } else {
        alert("can't play this kind of video");
      }
    });

    $play_button.on('click', function () {
      var $spans = $('span', this);

      if (video.paused) {
        video.play();
        $spans.removeClass("glyphicon-play");
        $spans.addClass("glyphicon-pause");
      } else {
        video.pause();
        $spans.addClass("glyphicon-play");
        $spans.removeClass("glyphicon-pause");
      }
    });

    $step_buttons.on("click", function () {
      var $button = $(this);
      var step_amount = $button.data('steps');

      // pause video if it is playing
      if (!video.paused) {
        $play_button.click();
      }

      video.currentTime = video.currentTime + step_amount;
    });
  }

  setup_video_in_container($compass_video_container);
  setup_video_in_container($shadow_video_container);



  // $step_backward_btn.on('click', function () {  //
  // $step_forward_btn.on('click', function () {
  //   video.currentTime = video.currentTime + step_increment;
  // });
  //
  // $step_backward_btn.on('click', function () {
  //   video.currentTime = video.currentTime - step_increment;
  // });
  //
  // $record_position_btn.on('click', function () {
  //   var degree = parseInt($degree_input.val());
  //   var video_time = video.currentTime;
  //
  //   var data = {
  //     'degree': degree,
  //     'video_time': video_time
  //   };
  //
  //   if (last_recorded_degree != null) {
  //     var delta = degree - last_recorded_degree;
  //     $degree_input.val(norm_degrees(degree + delta));
  //     data.degree_delta = delta;
  //   }
  //
  //   if (last_recorded_time != null) {
  //     var delta = video_time - last_recorded_time;
  //     var new_time = video_time + delta;
  //
  //     // Check we are not about to try to go beyond the end of the video.
  //     if (new_time > video.duration) { new_time = video.duration; }
  //     if (new_time < 0) { new_time = 0; }
  //
  //     // animate to the new position
  //     var number_of_steps = 5;
  //     var animation_duration = 0.5; // seconds
  //     var time_delta_per_step = delta / number_of_steps;
  //     var animate_interval = animation_duration / number_of_steps * 1000; // ms
  //
  //     var animate_step_forwards = function () {
  //       // console.log(video.currentTime, new_time);
  //       var next_step_time = video.currentTime + time_delta_per_step;
  //       if ( next_step_time > new_time) {
  //         // Video would step beyond where we want to be. Set video precisely
  //         // and stop.
  //         video.currentTime = new_time;
  //       } else {
  //         video.currentTime = next_step_time;
  //         setTimeout(animate_step_forwards, animate_interval);
  //       }
  //     };
  //     animate_step_forwards();
  //
  //     data.time_delta = delta;
  //   }
  //
  //   last_recorded_degree = degree;
  //   last_recorded_time   = video_time;
  //
  //   console.log(data);
  //   $('#data').append("<li>" + video_time + ", " + degree + "</li>");
  //
  // });
  //
  // $(document).keydown(function(e){
  //   var key = e.which;
  //   // console.log(key);
  //   if ( key === 39 ) {
  //     e.preventDefault();
  //     $step_forward_btn.click();
  //   } else if ( key === 37 ) {
  //     e.preventDefault();
  //     $step_backward_btn.click();
  //   } else if ( key === 40 ) {
  //     e.preventDefault();
  //     $record_position_btn.click();
  //   }
  //
  // });

});
