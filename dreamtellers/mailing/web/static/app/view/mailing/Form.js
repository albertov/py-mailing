Ext.define('WebMailing.view.mailing.Form', {
    extend: 'Ext.form.Panel',
    alias: 'widget.mailing_form',
    fieldDefaults: {
        labelAlign: 'top'
    },
    trackResetOnLoad: true,
    items: {
        xtype: 'container',
        layout: 'hbox',
        items: [
            {
                xtype: 'container',
                layout: 'anchor',
                items: [
                    {
                        fieldLabel: 'Número', //i18n
                        xtype: 'numberfield',
                        name: 'number',
                        anchor: '95%'
                    }
                ]
            }, {
                xtype: 'container',
                layout: 'anchor',
                items: [
                    {
                        fieldLabel: 'Fecha', //i18n
                        xtype: 'datefield',
                        format: 'Y/m/d',
                        name: 'date'
                    }
                ]
            }
        ]
    }
});

