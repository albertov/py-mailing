Ext.define('WebMailing.view.template.Panel', {
    extend: 'Ext.panel.Panel',
    requires: [
        'WebMailing.LoadMask',
        'Ext.layout.container.Border',
        'WebMailing.view.template.Grid',
        'WebMailing.view.template.Detail'
    ],
    alias: 'widget.templates',
    layout: 'border',
    items: [
        {
            xtype: 'template_grid',
            itemId: 'grid',
            region: 'west',
            width: 300,
            split: true,
            collapsible: true
        }, {
            xtype: 'template_form',
            itemId: 'form',
            region: 'center'
        }
    ],
    listeners: {
        activate: function() {
            var f = this.getCodeEditor();
            if (f.editor) {
                f.editor.focus();
            }
        }
    },
    modeMap: {
        'xhtml': 'text/html',
        'text': 'text/plain'
    },
    initComponent: function() {
        this.callParent(arguments);
        this.loadMask = Ext.create('WebMailing.LoadMask', this);
        Ext.getStore('Templates').on('update', this.onStoreUpdate, this);
    },
    getRecord: function() {
        return this.record;
    },
    getCodeEditor: function() {
        var fp = this.items.get('form');
        return fp.getForm().findField('body');
    },
    setRecord: function(record) {
        this.record = record;
        var fp = this.items.get('form'),
            mode = record?this.modeMap[record.get('type')]:null;
        if (record) {
            fp.setTitle(record.get('title'));
            fp.enable();
            this.getCodeEditor().setMode(mode);
            fp.getForm().loadRecord(record);
        } else {
            fp.disable();
            this.getCodeEditor().setValue('');
        }
    },
    onStoreUpdate: function(store, record) {
        if (record===this.record) {
            this.setRecord(record);
        }
    }
});
