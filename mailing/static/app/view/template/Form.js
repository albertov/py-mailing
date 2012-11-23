Ext.define('Mailing.view.template.Form', {
    extend: 'Ext.form.Panel',
    requires: [
        'Ext.form.Panel',
        'Ext.ux.codemirror.CodeMirror'
    ],
    alias: 'widget.template_form',
    title: '&nbsp;',
    trackResetOnLoad: true,
    bodyStyle: {
        padding: '5px'
    },
    items: [
        {
            xtype:      'codemirror',
            name:       'body',
            fieldLabel: 'Cuerpo', // i18n
            anchor:     '100% 0',
            hideLabel:  true,
            labelAlign: 'top',
            mode:       'text/html',
            showModes: false
        }
    ],
    disabled: true,
    buttons: [
        {
            text: 'Guardar', // i18n
            handler: function() {
                var form = this.up('form').getForm();
                if (form.isValid() && form.getRecord())
                    form.updateRecord();
            }
        }, {
            text: 'Cancelar', // i18n
            handler: function() {
                var form = this.up('form').getForm();
                form.reset();
            }
        }
    ]
});
