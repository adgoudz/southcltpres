
'use strict';

import '../scss/main.scss';

import 'modules/location';
import * as AOS from 'aos';

import focusBackground from 'utils/focus';


const defaultBackgroundWidth = 1900;
const defaultBackgroundHeight = 1267;


// Initialize animations
AOS.init({
    duration: 1200,
    easing: 'ease-out',
    offset: 50,
    once: true,
    disable: 'mobile'
});


// Focus hero on resize
$(window).resize(() => focusBackground($('#hero'), defaultBackgroundWidth, defaultBackgroundHeight));
