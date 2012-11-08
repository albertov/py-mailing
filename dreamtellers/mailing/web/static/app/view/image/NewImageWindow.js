Ext.define('WebMailing.view.image.NewImageWindow', {
    extend: 'Ext.window.Window',
    layout: 'fit',
    title: 'Nueva Imágen', //i18n
    alias: 'widget.new_image_window',
    width: 400,
    modal: true,
    items: {
        xtype: 'form',
        bodyPadding: 10,
        frame: true,
        items: [
            {
                xtype: 'textfield',
                name: 'title',
                fieldLabel: 'Título', //i18n
                allowBlank: true,
                anchor: '100%'
            }, {
                xtype: 'filefield',
                name: 'image',
                allowBlank: false,
                fieldLabel: 'Imágen', //i18n
                anchor: '100%',
                buttonText: 'Seleccionar imágen' // i18n
            }
        ],
        buttons: [
            {
                text: 'Crear', // i18n
                handler: function() {
                    var form = this.up('form').getForm(),
                        win = this.up('window');
                    if (form.isValid()) {
                        win.fireEvent('new', win);
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
