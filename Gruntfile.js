const sass = require('node-sass');

module.exports = function(grunt) {
  'use strict';

  require('load-grunt-tasks')(grunt);
  var productRoot = 'src/redturtle/infocard/browser/static';
  grunt.initConfig({
    sass: {
      options: {
        implementation: sass,
        sourceMap: true,
        outputStyle: 'compressed',
      },
      dist: {
        files: {
          // 'destination': 'source'
          './src/redturtle/infocard/browser/static/infocard.css': './src/redturtle/infocard/browser/static/infocard.scss',
        },
      },
    },
    cssmin: {
      target: {
        files: {
          './src/redturtle/infocard/browser/static/infocard-compiled.css': [
            `${productRoot}/infocard.css`
          ]
        }
      },
      options: {
        sourceMap: true
      }
    },
    postcss: {
      options: {
        map: {
          inline: false,
        },
        processors: [
          require('autoprefixer')({
            grid: true,
            browsers: ['last 2 versions', 'ie >= 11', 'iOS >= 6'],
          }),
          require('postcss-flexbugs-fixes')(),
        ]
      },
      dist: {
        src: [`${productRoot}/infocard.css`],
      },
    },
    watch: {
      css: {
        files: `${productRoot}/infocards.scss`,
        tasks: ['sass', 'postcss', 'cssmin'],
        options: {
          livereload: true
        }
      }
    }

  });

  grunt.registerTask('default', ['watch']);
  grunt.registerTask('compile', ['sass', 'postcss', 'cssmin']);
};
