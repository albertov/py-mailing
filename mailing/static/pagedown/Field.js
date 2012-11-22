Ext.define("Ext.ux.pagedown.Field", {
    extend: 'Ext.form.field.TextArea',
    alias: "widget.markdownfield",
    requires: [
        'Ext.form.field.TextArea'
    ],
    previewLabel: 'Previsualización', // i18n
    fieldSubTpl: [
        '<div>',
        '<div id="wmd-button-bar{cmpId}"></div>',
        '<textarea id="wmd-input{cmpId}" {inputAttrTpl}',
            '<tpl if="name"> name="{name}"</tpl>',
            '<tpl if="rows"> rows="{rows}" </tpl>',
            '<tpl if="cols"> cols="{cols}" </tpl>',
            '<tpl if="placeholder"> placeholder="{placeholder}"</tpl>',
            '<tpl if="size"> size="{size}"</tpl>',
            '<tpl if="maxLength !== undefined"> maxlength="{maxLength}"</tpl>',
            '<tpl if="readOnly"> readonly="readonly"</tpl>',
            '<tpl if="disabled"> disabled="disabled"</tpl>',
            '<tpl if="tabIdx"> tabIndex="{tabIdx}"</tpl>',
            ' class="{fieldCls} {typeCls}" ',
            '<tpl if="fieldStyle"> style="{fieldStyle}"</tpl>',
            ' autocomplete="off">\n',
            '<tpl if="value">{[Ext.util.Format.htmlEncode(values.value)]}</tpl>',
        '</textarea>',
        '<h2>{previewLabel}</h2>',
        '<div id="wmd-preview{cmpId}" class="wmd-preview"></div>',
        '</div>',
        {
            disableFormats: true
        }
    ],
    hookNames: [],
    initComponent: function() {
        this.inputId = 'wmd-input'+this.id;
        this.on('render', this._initializeEditor, this);
        this.addEvents("help");
        if (this.hookNames && this.hookNames.length) {
            this.addEvents.apply(this, this.hookNames);
        }
        this.callParent(arguments);
    },
    setValue: function() {
        this.callParent(arguments);
        if (this.editor) {
            this.editor.refreshPreview();
        }
    },
    getSubTplData: function() {
        return Ext.apply(this.callParent(), {
            previewLabel: this.previewLabel
        });
    },
    _initializeEditor: function() {
        var converter = new Markdown.getSanitizingConverter();
        this.editor = new Markdown.Editor(converter, this.id, {
            handler: Ext.bind(this.fireEvent, this, ["help", this])
        });
        var me = this;
        Ext.each(this.hookNames, function(hookName) {
            me.editor.hooks.set(hookName, function() {
                var args = [hookName].concat(Ext.Array.slice(arguments));
                return me.fireEvent.apply(me, args);
            });
        });
        this.editor.run();
    },
    getEditor: function() {
        return this.editor;
    }
});
