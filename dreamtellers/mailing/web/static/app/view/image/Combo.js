Ext.define('WebMailing.view.image.Combo', {
    extend: 'Ext.form.field.ComboBox',
    alias: 'widget.image_combo',
    forceSelection: true,
    tpl: [
        '<tpl for=".">',
            '<div class="x-boundlist-item">',
                '<span>{title}</span>',
                '<br />',
                '<img src="{url}?width=180&height=180" />',
            '</div>',
        '</tpl>'
    ],
    valueField: 'id',
    pageSize: 15,
    typeAhead: true,
    triggerAction: 'all',
    minChars: 1,
    listConfig: {
        minWidth: 200,
    },
    matchFieldWidth: false,
    queryMode: 'local',
    displayField: 'title',
    initComponent: function() {
        this.store = Ext.create('WebMailing.store.Images', {
            pageSize: this.pageSize||100,
            buffered: false
        });
        this.callParent(arguments);
        this.on('beforequery', function() {
            this.store.clearFilter();
            delete this.lastQuery;
        }, this);
    },
    doQuery: function(queryString, forceAll, rawQuery) {
        if (forceAll) {
            this.clearValue();
        }
        return this.callParent(arguments);
    },
    setValue: function(value) {
        // makes sure record is loaded in store
        if ( !this.store.loading &&
            (Ext.isNumber(value) || Ext.isString(value)) &&
            this.store.find(this.valueField, value)<0)
        {
            console.debug('setValue', value);
            this.store.load({
               filters: [{property: this.valueField, value:value}],
               page: 1,
               start: 0,
               limit: 1
            });
        }
        this.callParent(arguments);
    },
    assertValue: function() {
        // Allow blank selection
        if (this.getRawValue()) {
            this.callParent(arguments);
        }
    }
});
