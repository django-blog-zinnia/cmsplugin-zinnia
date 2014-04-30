var gulp       = require('gulp'),
    sass       = require('gulp-sass'),
    prefix     = require('gulp-autoprefixer'),
    livereload = require('gulp-livereload');

var HTML       = 'demo_cmsplugin_zinnia/templates/**/*.html',
    SASS       = 'demo_cmsplugin_zinnia/static/sass/*.scss',
    CSS        = 'demo_cmsplugin_zinnia/static/css/*.css';

gulp.task('sass', function() {

  return gulp.src(SASS)
         .pipe(sass())
         .pipe(prefix())
         .pipe(gulp.dest('demo_cmsplugin_zinnia/static/css'));
});

gulp.task('watch', function() {

  var server = livereload();

  gulp.watch(CSS, function(file) {
    server.changed(file.path);
  });

  gulp.watch(HTML, function(file) {
    server.changed('.');
  });

  gulp.watch(SASS, ['sass']);

});


gulp.task('default', ['sass', 'watch']);
