Ext.define('Mailing.view.template.TypeCombo', {
    extend: 'Ext.form.field.ComboBox',
    requires: [
        'Ext.form.field.ComboBox',
        'Ext.data.Store'
    ],
    alias: 'widget.template_type_combo',
    editable: false,
    queryMode: 'local',
    displayField: 'value',
    valueField: 'value',

    initComponent: function() {
        this.store = Ext.create('Ext.data.Store', {
            fields: ['value'],
            data: [
                {value: 'xhtml'},
                {value: 'text'}
            ]
        });
        this.callParent(arguments);
    }
});
