Ext.define('Mailing.view.template.UploadWindow', {
    extend: 'Ext.window.Window',
    layout: 'fit',
    title: 'Cargar plantilla', //i18n
    alias: 'widget.template_upload_window',
    width: 400,
    modal: true,
    requires: [
        'Ext.layout.container.Fit',
        'Ext.form.field.File',
        'Mailing.view.template.TypeCombo'
    ],
    items: {
        xtype: 'form',
        bodyPadding: 10,
        frame: true,
        items: [
            {
                xtype: 'template_type_combo',
                name: 'type',
                fieldLabel: 'Tipo' //i18n
            }, {
                xtype: 'filefield',
                name: 'body',
                allowBlank: false,
                fieldLabel: 'Plantilla', //i18n
                anchor: '100%'
            }
        ],
        buttons: [
            {
                text: 'Subir', // i18n
                handler: function() {
                    var form = this.up('form').getForm(),
                        win = this.up('window');
                    if (form.isValid()) {
                        win.fireEvent('upload', win, form);
                    }
                }
            }, {
                text: 'Cancelar', // i18n
                handler: function() {
                    this.up('window').close();
                }
            }
        ]
    }
});
