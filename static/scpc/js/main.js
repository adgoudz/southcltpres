
'use strict';

import '../scss/main.scss';

import 'modules/location';

import focusBackground from 'utils/focus';

const defaultBackgroundWidth = 1366;
const defaultBackgroundHeight = 911;


$(window).resize(() => focusBackground($('#hero'), defaultBackgroundWidth, defaultBackgroundHeight));


