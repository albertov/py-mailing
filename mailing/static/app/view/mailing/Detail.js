Ext.define('Mailing.view.mailing.Detail', {
    extend: 'Ext.tab.Panel',
    requires: [
        'Mailing.view.mailing.Edit',
        'Mailing.view.mailing.View',
        'Mailing.view.mailing_delivery.Panel'
    ],
    alias: 'widget.mailing_detail',
    title: '&nbsp;',
    record: null,
    disabled: true,
    items: [
        {
            itemId: 'view',
            xtype: 'tabpanel',
            title: 'Vista', // i18n
            tabConfig: {
                tooltip: 'Previsualización del boletín'
            },
            items: [
                {
                    itemId: 'html_view',
                    xtype: 'mailing_view',
                    view_type: 'xhtml',
                    title: 'HTML', // i18n
                    tabConfig: {
                        tooltip: 'Previsualización de la versión HTML.'
                    }
                }, {
                    itemId: 'text_view',
                    xtype: 'mailing_view',
                    view_type: 'text',
                    title: 'Texto', // i18n
                    tabConfig: {
                        tooltip: ('Previsualización de la versión básica.'+
                                  '<br />Ésta es la que verán los clientes '+
                                  'no puedan o no quieran mostrar HTML')
                    }
                }
            ]
        }, {
            itemId: 'edit',
            xtype: 'mailing_edit',
            title: 'Edición', //i18n
            tabConfig: {
                tooltip: ('Edición del boletín.<br />Aquí puede agregar '+
                          'artículos o enlaces, modificarlos, eliminarlos '+
                          'y reordenarlos')
            },
        }, {
            itemId: 'mailing_deliveries',
            xtype: 'mailing_deliveries',
            title: 'Envíos', //i18n
            tabConfig: {
                tooltip: ('Aquí puede programar nuevos envíos y ver el estado '+
                          'de los ya realizados')
            }
        }
    ],
    setRecord: function(record) {
        this.record = record;
        this.refresh();
    },
    getRecord: function() {
        return this.record;
    },
    refresh: function() {
        if (this.record) {
            this.down('#edit').setRecord(this.record);
            this.down('#mailing_deliveries').setRecord(this.record);
            this.down('#html_view').setRecord(this.record);
            this.down('#text_view').setRecord(this.record);
            this.setTitle(this.record.getTitle());
        }
    }
});
