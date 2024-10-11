create_db = """
                CREATE DATABASE vm_management;
            """

create_tables = """
                    CREATE TABLE v_machine(
                        vm_id SERIAL PRIMARY KEY,
                        ram_vol INT NOT NULL,
                        cpu_cores_amount INT
                    );


                    CREATE TABLE hard_drive(
                        hd_id SERIAL PRIMARY KEY,
                        vm_id INT,
                        memory_space INT NOT NULL,
                        CONSTRAINT fk_vm
                            FOREIGN KEY (vm_id)
                                REFERENCES v_machine(vm_id)
                                ON DELETE CASCADE
                    );

                    CREATE TABLE account(
                        acc_id SERIAL PRIMARY KEY,
                        login VARCHAR(255) NOT NULL,
                        password VARCHAR(255) NOT NULL,
                        CONSTRAINT fk_account
                            FOREIGN KEY(acc_id)
                            ON DELETE SET NULL
                    );

                    CREATE TABLE connection(
                        conn_id SERIAL PRIMARY KEY,
                        vm_id INT,
                        acc_id INT,
                        CONSTRAINT fk_vm
                            FOREIGN KEY v_machine(vm_id)
                            ON DELETE SET NULL
                        CONSTRAINT fk_acc
                            FOREIGN KEY account(acc_id)
                            ON DELETE SET NULL
                    );
                """

add_new_vm = """
                INSERT INTO v_machine(vm_id, ram_vol, cpu_cores)
                VALUES ($1, $2, $3);
             """

add_hd_device = """
                INSERT INTO hard_drive(hd_id, vm_id, memory_space)
                VALUES ($1, $2, $3);
                """

select_vms = """
                SELECT
                    vm.vm_id,
                    vm.ram_vol,
                    vm.cpu_cores
                FROM 
                    v_machine AS vm;
             """

update_vm = """
            UPDATE v_machine
            SET
                ram_vol = $1
                cpu_cores_amount = $2
            WHERE
                vm_id = $3;
            """

select_hds = """
                SELECT
                    *
                FROM
                    hard_drive;
             """

select_connectable_vms = """
                            SELECT
                                vm.vm_id,
                                vm.ram_vol,
                                vm.cpu_cores_amount
                            FROM
                                connection AS c
                            INNER JOIN
                                v_machine AS vm
                            ON
                                c.vm_id = vm.vm_id;
                         """

select_test = """
                SELECT * from staff;
              """