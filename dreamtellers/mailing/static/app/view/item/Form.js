Ext.define('WebMailing.view.item.Form', {
    extend: 'Ext.form.Panel',
    alias: 'widget.item_form',
    fieldDefaults: {
        labelAlign: 'top'
    },
    requires: [
        'Ext.ux.pagedown.Field',
        'Ext.container.Container',
        'Ext.layout.container.HBox',
        'Ext.form.field.ComboBox',
        'Ext.form.field.TextArea',
        'Ext.form.TextField'
    ],
    autoScroll: true,
    trackResetOnLoad: true,
    bodyStyle: {
        padding: '5px'
    },
    defaults: {
        anchor: '100%'
    },
    items: [
        {
            fieldLabel: 'Título', //i18n
            name: 'title',
            xtype: 'textarea',
            grow: 1
        }, {
            xtype: 'container',
            layout: 'hbox',
            items: [
                {
                    fieldLabel: 'Tipo', //i18n
                    name: 'type',
                    xtype: 'combo',
                    editable: false,
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
                    }),
                    flex: 1,
                    padding: "0 5 0 0"

                }, {
                    name: 'image_id',
                    xtype: 'image_combo',
                    fieldLabel: 'Imágen', //i18n
                    flex: 2
                }
            ]
        }, {
            fieldLabel: 'Enlace', //i18n
            name: 'url',
            vtype: 'url',
            xtype: 'textfield'
        }, {
            fieldLabel: 'Texto', //i18n
            name: 'content',
            xtype: 'markdownfield',
            grow: true,
            growMax: 250,
            hookNames: ["insertImageDialog"],
            listeners: {
                insertImageDialog: function(callback) {
                    var combo = this.up('form').getForm().findField('image_id'),
                        rec = combo.findRecordByValue(combo.getValue()),
                        mag = null;
                    if (rec) {
                        msg = "La plantilla insertará la imágen en el boletín";
                    } else {
                        msg = "Escoge una imágen para el Item en el menú del " +
                              "formulario.";
                    }
                    Ext.MessageBox.alert("Aviso", msg,
                                         function() {callback(null)});
                    return true;
                }
            }
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
