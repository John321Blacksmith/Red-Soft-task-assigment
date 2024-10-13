create_db = """
                CREATE DATABASE vm_management;
            """

create_tables = """
                    CREATE TABLE vm_management.public.v_machine(
                        vm_id serial PRIMARY KEY,
                        ram_vol INT NOT NULL,
                        cpu_cores_amount INT NOT NULL
                    );

                    CREATE table vm_management.public.hard_drive(
                        hd_id serial PRIMARY KEY,
                        vm_id INT,
                        memory_space INT NOT NULL,
                        FOREIGN KEY (vm_id)
                            REFERENCES vm_management.public.v_machine(vm_id)
                    );

                    CREATE TABLE vm_management.public.profile(
                        prof_id serial PRIMARY KEY,
                        login VARCHAR(255) UNIQUE NOT NULL,
                        password VARCHAR(255) UNIQUE NOT NULL
                    );

                    CREATE TABLE vm_management.public.connection(
                        conn_id serial PRIMARY KEY,
                        vm_id INT,
                        prof_id INT,
                        FOREIGN KEY (vm_id)
                            REFERENCES vm_management.public.v_machine(vm_id),
                        FOREIGN KEY (prof_id)
                            REFERENCES vm_management.public.profile(prof_id)
                    );
                """

create_new_vm = """
                INSERT INTO vm_management.public.v_machine(ram_vol, cpu_cores_amount)
                VALUES ($1, $2)
                RETURNING vm_id;
             """

create_hd_device = """
                INSERT INTO vm_management.public.hard_drive(vm_id, memory_space)
                VALUES ($1, $2)
                RETURNING hd_id;
                """

select_authorized_vms = """
                        SELECT
                            vm.vm_id,
                            vm.ram_vol,
                            vm.cpu_cores_amount,
                            sum(hd.memory_space) as overall_hd_space
                        FROM
                            vm_management.public.connection AS c
                        INNER JOIN
                            vm_management.public.v_machine as vm
                        ON
                            c.vm_id = vm.vm_id
                        INNER JOIN
                            vm_management.public.hard_drive AS hd
                        ON
                            vm.vm_id = hd.vm_id
                        WHERE
                            c.status = 'active'
                        GROUP BY
                            vm.vm_id;
                        """

select_vms = """
                SELECT
                    vm.vm_id,
                    vm.ram_vol,
                    vm.cpu_cores_amount
                FROM 
                    vm_management.public.v_machine AS vm;
             """

update_vm = """
            UPDATE vm_management.public.v_machine AS vm
            SET
                ram_vol = $1,
                cpu_cores_amount = $2
            FROM 
                vm_management.public.connection AS c
            WHERE
                vm.vm_id = $3
                AND c.status = 'active';
            """

logout_vm = """
            UPDATE vm_management.public.connection as c
            SET
                status=$1
            FROM
                vm_management.public.v_machine as vm
            WHERE
                vm.vm_id = c.vm_id
                AND vm.id = $2
                AND c.status = 'active';
            """

select_hds = """
                SELECT
                    *
                FROM
                     vm_management.public.hard_drive;
             """

select_connectable_vms = """
                            SELECT
                                vm.vm_id,
                                vm.ram_vol,
                                vm.cpu_cores_amount,
                                sum(hd.memory_space) as overall_hd_space
                            FROM
                                vm_management.public.connection AS c
                            INNER JOIN
                                vm_management.public.v_machine as vm
                            ON
                                c.vm_id = vm.vm_id
                            INNER JOIN
                                vm_management.public.hard_drive AS hd
                            ON
                                vm.vm_id = hd.vm_id
                            GROUP BY
                                vm.vm_id;
                         """

select_connected_vms = """
                            SELECT
                                vm.vm_id,
                                vm.ram_vol,
                                vm.cpu_cores_amount,
                                sum(hd.memory_space) as overall_hd_space
                            FROM
                                vm_management.public.connection AS c
                            INNER JOIN
                                vm_management.public.v_machine as vm
                            ON
                                c.vm_id = vm.vm_id
                            INNER JOIN
                                vm_management.public.hard_drive AS hd
                            ON
                                vm.vm_id = hd.vm_id
                            WHERE
                                c.status = 'active'
                            GROUP BY
                                vm.vm_id;
                        """

create_profile = """
                INSERT INTO  vm_management.public.profile(login, password)
                VALUES ($1, $2)
                RETURNING prof_id;
                """

create_connection = """
                    INSERT INTO  vm_management.public.connection(vm_id, prof_id, status)
                    VALUES($1, $2, 'active');
                    """

select_profile = """
                SELECT
                    *
                FROM
                     vm_management.public.profile
                WHERE
                    login = $1;
                """

set_conn_state = """
                UPDATE vm_management.public.connection AS c
                SET
                    status = $1
                FROM
                    vm_management.public.profile as prof
                WHERE
                    c.prof_id = prof.prof_id
                    AND prof.prof_id = $2;
                """