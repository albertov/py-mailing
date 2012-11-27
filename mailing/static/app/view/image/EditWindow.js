Ext.define('Mailing.view.image.EditWindow', {
    extend: 'Ext.window.Window',
    layout: 'fit',
    title: 'Editar imágen', //i18n
    alias: 'widget.image_edit_window',
    width: 400,
    modal: true,
    requires: [
        'Ext.layout.container.Fit',
        'Ext.form.field.File'
    ],
    items: {
        xtype: 'form',
        bodyPadding: 10,
        frame: true,
        items: [
            {
                xtype: 'filefield',
                name: 'data',
                allowBlank: false,
                fieldLabel: 'Actualizar fichero', //i18n
                anchor: '100%'
            }
        ],
        buttons: [
            {
                text: 'Subir nueva', // i18n
                tooltip: 'Subir un nuevo fichero para actualizar la imágen',
                handler: function() {
                    var form = this.up('form').getForm(),
                        win = this.up('window');
                    if (form.isValid()) {
                        win.fireEvent('upload', win, form);
                    }
                }
            //}, {
                //text: 'Cortar y escalar',
                //tooltip: 'Aplicar los cambios de encuadre y tamaño de imágen',
                //itemId: 'crop-scale'
            }, {
                text: 'Cancelar', // i18n
                handler: function() {
                    this.up('window').close();
                }
            }
        ]
    }
});
