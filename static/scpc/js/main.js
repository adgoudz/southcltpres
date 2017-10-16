
'use strict';

import '../scss/main.scss';

import 'modules/location';

import focusBackground from 'utils/focus';

const defaultBackgroundWidth = 1900;
const defaultBackgroundHeight = 1267;


// Focus hero on resize
$(window).resize(() => focusBackground($('#hero'), defaultBackgroundWidth, defaultBackgroundHeight));

// Hide alerts on close
$('.close').click((e) => { $(e.target).closest('.notice').slideUp() });
