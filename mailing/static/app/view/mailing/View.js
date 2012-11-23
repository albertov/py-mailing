Ext.define('Mailing.view.mailing.View', {
    extend: 'Mailing.IframePanel',
    requires: [
        'Mailing.store.Templates',
        'Ext.toolbar.Toolbar',
        'Ext.toolbar.TextItem',
        'Ext.form.field.ComboBox'
    ],
    alias: 'widget.mailing_view',
    view_type: 'xhtml',
    initComponent: function() {
        this.combo = Ext.widget('combo', {
            store: Ext.create('Mailing.store.Templates', {
                remoteFilter: true,
                autoLoad: true,
                filters: [
                    {property: 'type', value: this.view_type}
                ]
            }),
            queryCaching: false,
            displayField: 'title',
            valueField: 'id',
            forceSelection: true,
            triggerAction: 'all',
            editable: false,
            dock: 'top'
        });
        this.callParent(arguments);
        this.addDocked(Ext.widget('toolbar', {
            items: [
                Ext.widget('button', {
                    iconCls: 'x-tbar-loading',
                    handler: function() {
                        this.up('mailing_view').reload();
                    },
                    tooltip: 'Recargar la vista del Boletín' //i18n
                }),
                Ext.widget('tbtext', {
                    text:'Plantilla' // i18n
                }), 
                this.combo
            ]
        }));
    },
            
    setRecord: function(record) {
        if (record) {
            this.setSrc(record.getViewUrl(this.view_type));
        }
        if (this.record!==record) {
            this.record = record;
            var me = this;
            this.record.getTemplate(this.view_type, function(tpl) {
                me.combo.select(tpl?tpl.get('id'):null);
            });
        }
    },

    getRecord: function() {
        return this.record;
    }
});
