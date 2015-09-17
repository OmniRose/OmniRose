jQuery(function ($) {
  console.log('starting');

  var $file_input = $("#file_input");
  var $degree_input = $("#degree_input");
  var video = $("video")[0];

  var $step_forward_btn  = $('#step_forward_btn');
  var $step_backward_btn = $('#step_backward_btn');
  var $record_position_btn = $('#record_position_btn');

  // The amount of time to move forwards and backwards in the video. Slightly
  // less than what is needed to see every frame in a 30fps video.
  var step_increment = 0.03;

  var last_recorded_degree = null;
  var last_recorded_time   = null;

  var norm_degrees = function (degree) {
    return (degree + 360) % 360;
  };

  $file_input.on('change', function (event) {
    var file = this.files[0];
    console.debug(file, file.type);

    // check that we can play this sort of file
    if (video.canPlayType(file.type)) {
      console.log('can play video');
      var fileURL = URL.createObjectURL(file);
      video.src = fileURL;
    } else {
      alert("can't play this kind of video");
    }

  });

  $(video).on('timeupdate', function () {
    $('#video_current_time').html(video.currentTime);
  });

  $step_forward_btn.on('click', function () {
    video.currentTime = video.currentTime + step_increment;
  });

  $step_backward_btn.on('click', function () {
    video.currentTime = video.currentTime - step_increment;
  });

  $record_position_btn.on('click', function () {
    var degree = parseInt($degree_input.val());
    var video_time = video.currentTime;

    var data = {
      'degree': degree,
      'video_time': video_time
    };

    if (last_recorded_degree != null) {
      var delta = degree - last_recorded_degree;
      $degree_input.val(norm_degrees(degree + delta));
      data.degree_delta = delta;
    }

    if (last_recorded_time != null) {
      var delta = video_time - last_recorded_time;
      var new_time = video_time + delta;

      // animate to the new position
      var number_of_steps = 5;
      var animation_duration = 0.5; // seconds
      var time_delta_per_step = delta / number_of_steps;
      var animate_interval = animation_duration / number_of_steps * 1000; // ms

      var animate_step_forwards = function () {
        if (video.currentTime < new_time) {
          video.currentTime = video.currentTime + time_delta_per_step;
          setTimeout(animate_step_forwards, animate_interval);
        } else {
          video.currentTime = new_time;
        }
      };
      animate_step_forwards();

      data.time_delta = delta;
    }

    last_recorded_degree = degree;
    last_recorded_time   = video_time;

    console.log(data);
    $('#data').append("<li>" + video_time + ", " + degree + "</li>");

  });

  $(document).keydown(function(e){
    var key = e.which;
    // console.log(key);
    if ( key === 39 ) {
      e.preventDefault();
      $step_forward_btn.click();
    } else if ( key === 37 ) {
      e.preventDefault();
      $step_backward_btn.click();
    } else if ( key === 40 ) {
      e.preventDefault();
      $record_position_btn.click();
    }

  });

});
