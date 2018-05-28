from globals import *

TYPES = {
	'none': {
		'icon': ' ',
		'color': [BACKGROUND_COLOR],
		'background': [BACKGROUND_COLOR],
		'font': FONT_REG
	},
	'floor': {
		'icon': '.',
		'color': [
			'000055', 
			'000055',
			'222222',
			'666666'
		],
		'background': [FLOOR_COLOR],
		'font': FONT_REG
	},
	'wall': {
		'icon': '#',
		'color': ['0f0f0f'],
		'background': [
			'052A6E',
			'29477F',
			'062270',
			'133CAC'
		],
		'font': FONT_REG
	},
	'door': {
		'icon': '+',
		'color': ['ff0000'],
		'background': ['bbbbbb'],
		'font': FONT_ITL
	},
	'grass': {
		'icon': '.',
		'color': [
			'00B060', 
			'218457',
			'00733E',
			'006E4A',
			'228A4C',
		],
		'background': [FLOOR_COLOR],
		'font': FONT_REG
	},
	'tall grass': {
		'icon': '~',
		'color': [
			'00B060', 
			'218457',
			'00733E',
			'006E4A',
			'228A4C',
		],
		'background': [FLOOR_COLOR],
		'font': FONT_REG
	},
	'water': {
		'icon': '.',
		'color': ['ffffff'],
		'background': [
			'086CA2', 
			'3C9DD0',
			'39AECF',
			'057D9F',
			'64AAD0',
		],
		'font': FONT_REG
	},
	'deep water': {
		'icon': '~',
		'color': ['ffffff'],
		'background': [
			'086CA2', 
			'3C9DD0',
			'39AECF',
			'057D9F',
			'64AAD0',
		],
		'font': FONT_REG
	},
	'red mushroom floor': {
		'icon': '.',
		'color': [
			'ff0000',
			'B52D43',
			'970026',
			'F10026',
			'BF5730',
			'A62D00'
		],
		'background': [FLOOR_COLOR],
		'font': FONT_REG
	},
	'red mushroom': {
		'icon': '*',
		'color': [
			'ff0000',
			'B52D43',
			'970026',
			'F10026',
			'BF5730',
			'A62D00'
		],
		'background': [FLOOR_COLOR],
		'font': FONT_REG
	},
	'purple mushroom floor': {
		'icon': '.',
		'color': [
			'C936D3',
			'65016C',
			'77207D',
			'7908AA',
		],
		'background': [FLOOR_COLOR],
		'font': FONT_REG
	},
	'purple mushroom': {
		'icon': '*',
		'color': [
			'C936D3',
			'65016C',
			'77207D',
			'7908AA',
		],
		'background': [FLOOR_COLOR],
		'font': FONT_REG
	}
}