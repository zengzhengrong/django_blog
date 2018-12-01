/**
 * @license Copyright (c) 2003-2017, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.md or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here. For example:
	// config.language = 'fr';
	// config.uiColor = '#AADC6E';
	// 回车换行，shift回车添加p标签
	 config.enterMode = CKEDITOR.ENTER_BR; 
	 config.shiftEnterMode = CKEDITOR.ENTER_P;
	 // 取消img插件中的默认宽高样式
	 config.disallowedContent = 'img{wieth,height};img[wieth,height]';
};
