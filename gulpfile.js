var gulp       = require('gulp'),
    sass       = require('gulp-sass'),
    prefix     = require('gulp-autoprefixer'),
    livereload = require('gulp-livereload');

var HTML       = 'templates/**/*.html',
    SASS       = 'cmsplugin_zinnia/static/cmsplugin_zinnia/sass/**/*.scss',
    CSS        = 'cmsplugin_zinnia/static/cmsplugin_zinnia/css/*.css';

gulp.task('sass', function() {

  return gulp.src(SASS)
         .pipe(sass())
         .pipe(prefix())
         .pipe(gulp.dest('cmsplugin_zinnia/static/cmsplugin_zinnia/css'));
});

gulp.task('watch', function() {

  var server = livereload();

  gulp.watch([HTML, CSS], function(file) {
    server.changed(file.path);
  });

  gulp.watch(SASS, ['sass']);

});


gulp.task('default', ['sass', 'watch']);
