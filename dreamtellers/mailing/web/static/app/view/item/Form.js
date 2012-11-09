Ext.define('WebMailing.view.item.Form', {
    extend: 'Ext.form.Panel',
    alias: 'widget.item_form',
    fieldDefaults: {
        labelAlign: 'top'
    },
    requires: [
        'Ext.ux.pagedown.Field'
    ],
    autoScroll: true,
    trackResetOnLoad: true,
    bodyStyle: {
        padding: '5px'
    },
    items: [
        {
            name: 'type',
            xtype: 'combo',
            editable: false,
            fieldLabel: 'Tipo', //i18n
            anchor: '95%',
            queryMode: 'local',
            displayField: 'text',
            valueField: 'value',
            store: Ext.create('Ext.data.Store', {
                fields: ['value', 'text'],
                data: [
                    {
                        value: 'Article',
                        text: 'Artículo' // i18n
                    }, {
                        value: 'ExternalLink',
                        text: 'Enlace' //i18n
                    }
                ]
            })

        }, {
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
            name: 'image_id',
            xtype: 'image_combo',
            fieldLabel: 'Imágen', //i18n
            anchor: '95%'
        }, {
            name: 'content',
            xtype: 'markdownfield',
            grow: true,
            growMax: 250,
            fieldLabel: 'Texto', //i18n
            anchor: '95%'
        }
    ],
    buttons: [
        {
            text: 'Guardar', // i18n
            handler: function() {
                var form = this.up('form').getForm();
                if (form.isValid())
                    form.updateRecord();
            }
        }, {
            text: 'Cancelar', // i18n
            handler: function() {
                var form = this.up('form').getForm();
                form.reset();
            }
        }
    ],
    initComponent: function() {
        this.callParent(arguments);
        this.getForm().findField('type').on('select', this.onTypeChange, this);
    },
    onTypeChange: function(field) {
        this.setupFieldsForType(field.getValue());
    },
    disable: function() {
        this.items.each(function(f) {f.hide()});
        this.callParent(arguments)
    },
    loadRecord: function(record) {
        this.enable();
        this.setupFieldsForType(record.get('type'));
        this.callParent(arguments);
    },
    setupFieldsForType: function(type) {
        var funcName = 'setupFieldsFor'+type;
        var func = this[funcName];
        if (func) {
            this.items.each(function(f) {f.enable(); f.show()});
            func.call(this);
        } else {
            this.disable();
        }
    },
    setupFieldsForArticle: function() {
        var url = this.getForm().findField('url')
        url.allowBlank = true;
        url.hide();
        var content = this.getForm().findField('content')
        content.allowBlank = false;
    },

    setupFieldsForExternalLink: function() {
        var url = this.getForm().findField('url')
        url.allowBlank = false;
        var content = this.getForm().findField('content')
        content.allowBlank = true;
    }

});
