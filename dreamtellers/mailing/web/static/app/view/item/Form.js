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
            anchor: '95%'
        }, {
            name: 'url',
            xtype: 'textfield',
            fieldLabel: 'Enlace', //i18n
            anchor: '95%'
        }, {
            name: 'content',
            xtype: 'textareafield',
            grow: true,
            growMax: 400,
            fieldLabel: 'Texto', //i18n
            anchor: '95%'
        }
    ],
    loadRecord: function(record) {
        this.setupFieldsForType(record.get('type'));
        this.callParent(arguments);
    },
    setupFieldsForType: function(type) {
        var funcName = 'setupFieldsFor'+(type||'Category');
        var func = this[funcName];
        if (func) {
            this.items.each(function(f) {f.enable(); f.show()});
            func.call(this);
        } else {
            this.items.each(function(f) {f.disable()});
        }
    },
    setupFieldsForArticle: function() {
        this.getForm().findField('url').hide();
    },

    setupFieldsForCategory: function() {
        this.getForm().findField('content').hide();
        this.getForm().findField('url').hide();
    },
    setupFieldsForExternalLink: function() {
    }

});
