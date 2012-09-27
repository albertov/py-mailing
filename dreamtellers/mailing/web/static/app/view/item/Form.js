Ext.define('WebMailing.view.item.Form', {
    extend: 'Ext.form.Panel',
    alias: 'widget.item_form',
    fieldDefaults: {
        labelAlign: 'top'
    },
    items: [
        {
            name: 'title',
            xtype: 'textfield',
            fieldLabel: 'Título', //i18n
            anchor: '95%',
        }, {
            name: 'url',
            disabled: true,
            xtype: 'textfield',
            fieldLabel: 'Enlace', //i18n
            anchor: '95%',
        }, {
            name: 'text',
            xtype: 'textareafield',
            fieldLabel: 'Texto', //i18n
            anchor: '95%',
        }
    ],
    loadRecord: function(record) {
        this.setupFieldsForType(record.get('type'));
        this.callParent(arguments);
    },
    setupFieldsForType: function(type) {
        var func = this['setupFieldsFor'+type];
        if (func) {
            func.call(this);
        } else {
            this.fields.each(function(f) {f.disable()});
        }
    },
    setupFieldsForArticle: function() {
        this.findField('url').disable();
    }

});
