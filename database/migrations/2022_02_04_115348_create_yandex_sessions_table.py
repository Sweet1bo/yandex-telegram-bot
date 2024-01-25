from orator.migrations import Migration


class CreateYandexSessionsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('yandex_sessions') as table:
            table.increments('id')
            table.integer('park_id').unsigned()
            table.foreign('park_id').references('id').on('parks')
            table.text('session')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('yandex_sessions')
