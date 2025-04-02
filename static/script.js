/**
 * La función `createProject` envía una petición POST para generar un proyecto con un nombre dado, muestra
 * mensajes de carga y alertas de éxito/error usando SweetAlert, y maneja los errores de conexión al servidor.
 */
function createProject() {
    let projectName = document.getElementById("project-name").value;
    let button = document.getElementById("Button-create");
    //document.getElementById("database-section").style.display = "flex";
    Swal.fire({
        title: 'Creando el proyecto...',
        text: 'Por favor, espera mientras se generan los archivos.',
        allowOutsideClick: false,
        heightAuto: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });

    fetch("/generate_project", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            project: projectName
        })
    }).then(response => response.json())
        .then(data => {
            Swal.close();

            if (data.success) {
                Swal.fire({
                    icon: 'success',
                    title: 'Creado',
                    text: data.message,
                    heightAuto: false
                });

                projectName.disabled = true;
                button.disabled = true;
                button.style.backgroundColor = "#4f8dce";
                // Mostrar la sección de la base de datos
                document.getElementById("database-section").style.display = "flex";
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: data.message,
                    heightAuto: false
                });
            }
        }).catch(error => {
            Swal.close();
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Error de conexión con el servidor.',
                heightAuto: false
            });
        });
}

/**
 * La función `testDatabase` en JavaScript comprueba la información de conexión a la base de datos requerida, envía
 * una solicitud POST para probar la conexión a la base de datos, y muestra el mensaje de resultado en consecuencia.
 * La función `testDatabase()` devuelve un mensaje de éxito indicando que la conexión a la base de datos se ha realizado correctamente 
 * o un mensaje de error si se ha producido algún problema durante la conexión.
 * La función `testDatabase()` devuelve un mensaje de éxito indicando que la conexión a la base de datos es correcta o un 
 * mensaje de error si hay algún problema durante la prueba de conexión a la base de datos.
 * Los mensajes específicos que pueden ser devueltos son:
 * - «Conexión exitosa a la base de datos». (Conexión exitosa a la base de datos)
 * - «Error: [mensaje de error]» (Mensaje de error recibido del servidor)
 * - «Error de conexión con el servidor» (Error de conexión con el servidor)
 * - «Todos los campos son obligatorios» (Cuando no se han completado todos los campos requeridos)
 */
function testDatabase() {
    let message = document.getElementById("db-message");

    let dbName = document.getElementById("db").value;
    let user = document.getElementById("user").value;
    let password = document.getElementById("password").value;
    let host = document.getElementById("host").value;
    let port = document.getElementById("port").value;

    if (!dbName || !user || !password || !host || !port) {
        message.innerText = "Todos los campos son obligatorios.";
        message.style.color = "red";
        message.style.display = "block";
        return;
    }

    fetch("/test_db", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            db: dbName,
            user: user,
            password: password,
            host: host,
            port: port
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                message.innerText = "Conexión exitosa a la base de datos.";
                message.style.color = "green";
                message.style.display = "block";
                showTables(data.tables);
            } else {
                message.innerText = "Error: " + data.message;
                message.style.color = "red";
                message.style.display = "block";
            }
        })
        .catch(error => {
            message.innerText = "Error de conexión con el servidor.";
            message.style.color = "red";
            message.style.display = "block";
        });
}

/**
 * La función `showTables` muestra una lista de tablas de una base de datos en una página web con casillas de verificación
 * para la selección.
 * @param tables - Un array de arrays, donde cada array interior representa una tabla de una base de datos. Cada
 * contiene el nombre de la tabla como primer elemento y el primer atributo de la tabla como segundo elemento.
 * segundo elemento.
 * @returns Si el array `tables` está vacío, la función devolverá un mensaje diciendo «No hay tablas en
 * la base de datos». De lo contrario, mostrará una lista de tablas con casillas de verificación junto a cada tabla
 * nombre.
 */
function showTables(tables) {
    let tableContainer = document.getElementById("tables-list");
    tableContainer.innerHTML = "";

    if (tables.length === 0) {
        tableContainer.innerHTML = "<p>No hay tablas en la base de datos.</p>";
        return;
    }

    tables.forEach(([tableName, firstAttribute]) => {
        let div = document.createElement("div");
        div.classList.add("table-row");
        div.innerHTML = `<input class="input-table" type="checkbox" name="${firstAttribute}" value="${tableName}">
                         <span>${tableName}</span>`;
        tableContainer.appendChild(div);
    });

    document.getElementById("database-tables").style.display = "block";
}

/**
 * La función `checks_all` gestiona la marcación y desmarcación de casillas de verificación en una tabla basada en una
 * select-all checkbox.
 */
function checks_all() {
    const selectAllCheckbox = document.getElementById("select-all");
    const tableCheckboxes = document.querySelectorAll(".input-table");
    const tableContainer = document.getElementById("tables-list");

    tableCheckboxes.forEach(checkbox => {
        checkbox.checked = selectAllCheckbox.checked;
    });

    tableContainer.addEventListener("change", function (event) {
        if (event.target.classList.contains("input-table")) {
            if (!event.target.checked) {
                selectAllCheckbox.checked = false;
            } else {
                const allChecked = [...tableCheckboxes].every(checkbox => checkbox.checked);
                selectAllCheckbox.checked = allChecked;
            }
        }
    });
}

/**
 * La función `tables_generate` selecciona las tablas seleccionadas, envía una petición POST para generar archivos 
 * basados en las tablas seleccionadas y muestra mensajes de éxito y error usando SweetAlert.
 * en las tablas seleccionadas, y muestra mensajes de éxito o error usando SweetAlert.
 * @returns La función `tables_generate` devuelve un mensaje de alerta si no hay tablas seleccionadas o realiza una 
 * petición POST para generar archivos basados en las tablas seleccionadas.
 * Dependiendo de la respuesta del servidor, se mostrará un mensaje de éxito si los archivos se han 
 * generado con éxito, un mensaje de error si hubo un problema generando los archivos, o un mensaje de advertencia
 * mensaje de advertencia si hubo un error de conexión
 */
function tables_generate() {
    const tables = document.querySelectorAll(".input-table");
    const selectedTables = [];

    tables.forEach(table => {
        if (table.checked) {
            selectedTables.push({
                table: table.value,
                first_attribute: table.name
            });
        }
    });

    if (selectedTables.length === 0) {
        alert("Debe seleccionar al menos una tabla.");
        return;
    }

    fetch('/generate_tables', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            tables: selectedTables
        })
    }).then(response => response.json())
        .then(data => {
            if (data.success) {
                Swal.fire({
                    icon: 'success',
                    title: 'Éxito',
                    text: 'Archivos generados exitosamente.',
                    heightAuto: false,
                });
                tables.forEach(table => {
                    if (table.checked) {
                        table.checked = false;
                        table.disabled = true;
                    }
                });
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Error al generar los archivos.',
                    heightAuto: false,
                });
            }
        })
        .catch(error => {
            Swal.fire({
                icon: 'warning',
                title: 'Error de conexión',
                text: 'Error de conexión con el servidor.',
                heightAuto: false,
            });
        });
}

/**
 * La función `run` envía una petición POST a «/run_server» y desactiva un botón con id «Button-run»
*/
function run() {
    let button_server = document.getElementById("Button-run");

    fetch("/run_server", {
        method: "POST",
    })
    button_server.disabled = true;
    button_server.style.backgroundColor = "#1aaf3c";

}

/**
 * La función `Project` oculta el elemento con el id «container-0-section» y muestra el elemento
 * con el id «project-section».
 */
function Project() {
    document.getElementById("container-0-section").style.display = "none";
    document.getElementById("project-section").style.display = "block";
}


/**
 * La función `Audit` oculta una sección y muestra otra sección en una página web.
 */
function Audit() {
    document.getElementById("container-0-section").style.display = "none";
    document.getElementById("database-section-audit").style.display = "flex";
}

/**
 * La función alterna la visualización de dos secciones en función de su visibilidad actual.
 */
function back() {
    let project_section = document.getElementById("project-section")
    let database_section = document.getElementById("database-section-audit")
    if (project_section.style.display == "block") {
        project_section.style.display = "none"
    } else {
        database_section.style.display = "none"
    }
    document.getElementById("container-0-section").style.display = "flex";
}

/**
 * La función `testDatabaseAudit` en JavaScript envía una petición POST para probar una conexión a una base de datos
 * y muestra el mensaje de resultado en consecuencia.
 * @returns La función `testDatabaseAudit` devuelve una Promise. Esta Promise está manejando la
 * La función envía una petición POST a la base de datos. La función envía una petición POST a
 * «/test_db_audit» con las credenciales de la base de datos proporcionadas por el usuario. La respuesta del servidor
 * servidor es procesada para mostrar un mensaje de éxito con información de la tabla si la prueba es
 * con éxito, o un mensaje de error si hay un problema con la conexión. Si hay un error de conexión con el servidor,
 * se muestra un mensaje de error de conexión.
 */
function testDatabaseAudit() {
    let message = document.getElementById("db-message-audit");

    let dbName = document.getElementById("db-audit").value;
    let user = document.getElementById("user-audit").value;
    let password = document.getElementById("password-audit").value;
    let host = document.getElementById("host-audit").value;
    let port = document.getElementById("port-audit").value;

    if (!dbName || !user || !password || !host || !port) {
        message.innerText = "Todos los campos son obligatorios.";
        message.style.color = "red";
        message.style.display = "block";
        return;
    }

    fetch("/test_db_audit", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            db: dbName,
            user: user,
            password: password,
            host: host,
            port: port
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                message.innerText = data.message;
                message.style.color = "green";
                message.style.display = "block";
                //document.getElementById("form-db-audit").style.display = "none";
                showTablesAudit(data.tables);
            } else {
                message.innerText = "Error: " + data.message;
                message.style.color = "red";
                message.style.display = "block";
            }
        })
        .catch(error => {
            message.innerText = "Error de conexión con el servidor.";
            message.style.color = "red";
            message.style.display = "block";
        });
}

/**
 * La función `showTablesAudit` muestra una lista de tablas con una opción para realizar una auditoría en cada una de ellas.
 * tabla.
 * @param tables - La función `showTablesAudit` toma un array de tablas como parámetro. Cada tabla
 * en la matriz se representa como una matriz con dos elementos: el nombre de la tabla y el primer atributo de la tabla.
 * de la tabla.
 * @return La función `showTablesAudit` devuelve la lista de tablas con un botón «Auditoria» al lado de cada nombre de tabla.
 * junto al nombre de cada tabla. El botón dispara la función `realizarAuditoria` con el nombre de la tabla * encriptada como parámetro cuando se pulsa.
 * encriptada como parámetro.
 */
function showTablesAudit(tables) {
    const encryptedTableNames = {
        "extractos_bancarios": "t_bd0c503356edc5ba780920ee53000e4bae258e03852542f5562d6486ac3460f6",
        "pisos_bloques": "t_fb35d3a68a11c154b17749ab79b0330a",
        "ambientes": "t_bab74159bec4343d662afe4fced1e2ef",
        "universidades": "t_dac7469891f477eb03c686ace88f6c6f",
        "areas": "t_a9666f8cdddd8e86ff93b3deec276811",
        "edificios": "t_373762f3b4acf7198542e5fe157e16c5",
        "bloques": "t_d42f8478bcc47ecb661a35f03f868d88",
        "carreras_niveles_academicos": "t_cacf68e384ebd40f8e07f83334f4e7693d5268aa82db6685d13e2a473450afb1",
        "carreras": "t_77342fe4107dc13d2c4446fe8f72f1ca",
        "facultades": "t_9bd172379dbabb4b484783c708d8ad2e",
        "modalidades": "t_956893ee115586e5eec0eeb4b16db536",
        "sedes": "t_e62407297c8557fceb5eea629bfdb463",
        "configuraciones": "t_4292ae7a5be523185c1b4b458fecb4a4",
        "cuentas_cargos_posgrados_conceptos": "t_fe03f8a7995c367578a3b0137b4ec8adfb9cbf02f930e5a3291cf2c4efc2c1385ef26f811a4ec15858bf629c241a72f6",
        "cuentas_cargos_conceptos_posgrados": "t_1e00be2799a6afff178d47353e67ba0a90759d80d8f5bb4a015db69c266ecce17ac95eb705baa7dd4708162f8f2fbcf5",
        "posgrados_programas": "t_8377f8e6724f71658db4a9b8595ef1b7531ee09565d43422d33faf2d77955493",
        "cuentas_cargos_posgrados": "t_fe03f8a7995c367578a3b0137b4ec8adc957e298d54947cac30e0d80b80a0a02",
        "cuentas_conceptos": "t_f06c16be0e84d3afd5f862c1159a54ac94d9668fc38005f41ab95e921dcc6f25",
        "paises": "t_ce367b3d5be32e60964f0907543938e8",
        "departamentos": "t_13e70efae39eb4803b2a37fee3a6a9c0",
        "campus": "t_9d3e727e46a5fb129578076b26a4865a",
        "facultades_edificios": "t_07df6506ff392641ed54d7165446efd07e542d73a30bc39fbe54c0327b7774de",
        "provincias": "t_68896d5dcc74dc35bffd58e286fc05e5",
        "localidades": "t_e15aed7c33d1042bcd1475f3ee0aedc4",
        "menus_principales": "t_d77b48e4ab45b21ee67102b54b1bc90ed911b2124bce157656dccfbf09dc772f",
        "menus": "t_7667f201dfab29989aaa4527ba0ad748",
        "modulos": "t_11f742c904a0ebb0a1c0f18170d1a2b7",
        "grupos_sanguineos": "t_799325bea925e5e1b378b3d6313671656ed34cdad42ca2c65ba43a09f186364d",
        "posgrados_transacciones_detalles": "t_1dacfb080c0c48c9098d6c3343bf5bed3626e9efb42ed73754d0dfd34d352d994c6857cd4b0f779121ca06618ab61e4a",
        "montos_excedentes": "t_139bf4b75640298fb89b5f8552fe4edd449cda7f53bd83571cc64c844a5a8706",
        "niveles_academicos": "t_7c3ae84ff7875aebe38691dfdbd6aa872f30709db8ec26603f986db8d6657fec",
        "niveles_academicos_tramites_documentos": "t_7c3ae84ff7875aebe38691dfdbd6aa879fa5a0c1f8ba78e2919a413d2269f333dd3297c552dec55bcbd1080e16e52f75",
        "emision_cedulas": "t_c869bcc50d9da570ad044a59ec655e91",
        "personas": "t_e493f6921425c6b69bc64f7e746dd2e9",
        "estados_civiles": "t_29b7a8229f1bfe3c5558bf90381ff5f2",
        "sexos": "t_68bfa097b6098609b72059aac70952d1",
        "personas_administrativos": "t_c3c53ab66ef5277ada23792bf1693ea663bd390bbe45c0d0536babddd3d3c26c",
        "personas_alumnos": "t_155230f9dce86c1fd23b999236b43be1726b29c30a797a92ca06c44d170b6944",
        "personas_alumnos_posgrados": "t_155230f9dce86c1fd23b999236b43be1841ef9976d52a0472e05434247188fb4",
        "personas_decanos": "t_ad668aa30cb063f06101123faf627329fadfac1f8b3deb88cd282a5e479b2877",
        "personas_directores_carreras": "t_158cca3478a6f5d1a8208187e5adc7a4522cd97da2891ef5dad76ff927d7cd5c",
        "personas_directores_posgrados": "t_158cca3478a6f5d1a8208187e5adc7a47a29a2ddb63e4fd2bc9bcbfb051e6f1d",
        "personas_docentes": "t_168ceaf6dc5e404e8240abc288c8c4e97b01460a2cc630aaef8d6ce0b3b6996e",
        "personas_facultades_administradores": "t_12b03d0236f1c210f612db8b382ed3a77c89ab13f473c6ef76e0f015627da902b6e88410385d6cb84a15fb24e8aff0fc",
        "personas_roles": "t_34ccef3f31d73aafbd13085e04664115",
        "roles": "t_1f9cd962ab78ff8d73741be020b6b3ae",
        "pisos": "t_3d7f5b94c9d8466b7612827ebdf5adf4",
        "usuarios": "t_abf98aeaeb7aefdaca3fcd19cd0f62e8"
    };

    let tableContainer = document.getElementById("tables-list-audit");
    tableContainer.innerHTML = "";

    if (tables.length === 0) {
        tableContainer.innerHTML = "<p>No hay tablas en la base de datos.</p>";
        return;
    }

    tables.forEach(([tableName, firstAttribute]) => {
        let div = document.createElement("div");
        div.classList.add("table-row-audit");

        let tableNameSpan = `<span class="table-name-span">${tableName}</span>`;

        let auditButton = document.createElement("button");
        auditButton.id = "audit-button";
        auditButton.textContent = "Auditoria";
        auditButton.dataset.encryptedName = encryptedTableNames[tableName] || "N/A";
        auditButton.onclick = function () {
            realizarAuditoria(this.dataset.encryptedName);
        };

        div.innerHTML = tableNameSpan;
        div.appendChild(auditButton);

        tableContainer.appendChild(div);
    });


    document.getElementById("database-tables-audit").style.display = "block";
}

/**
 * La función `realizarAuditoria` realiza una auditoría enviando una petición POST con información de la base de datos.
 * información de la base de datos, luego procesa los datos de respuesta para mostrar una tabla en un modal usando SweetAlert.
 * @param encryptedName - El parámetro `encryptedName` de la función `realizarAuditoria` representa
 * el nombre de la tabla que ha sido encriptada para propósitos de auditoría. Este nombre se utilizará como parte
 * de la carga útil de la solicitud enviada al servidor cuando se generen tablas de auditoría.
 */
function realizarAuditoria(encryptedName) {
    let dbName = document.getElementById("db-audit").value;
    let user = document.getElementById("user-audit").value;
    let password = document.getElementById("password-audit").value;
    let host = document.getElementById("host-audit").value;
    let port = document.getElementById("port-audit").value;

    fetch("/generate_audit_tables", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            db: dbName,
            user: user,
            password: password,
            host: host,
            port: port,
            table_name: encryptedName
        })
    })
        .then(response => response.json()) // Parsear la respuesta como JSON
        .then(data => {
            if (data.success) {
                let columns = data.result.columns;
                let rows = data.result.data;
            
                // Definir el orden deseado (sin action y action_date al inicio)
                const fixedOrder = columns.filter(col => col !== "action" && col !== "action_date");
                fixedOrder.push("action", "action_date"); // Agregar al final
            
                // Reordenar los datos de cada fila según el nuevo orden de columnas
                let reorderedRows = rows.map(row => {
                    let reorderedRow = fixedOrder.map(col => row[columns.indexOf(col)]);
                    return reorderedRow;
                });
            
                // Construir la tabla en HTML
                let tableHTML = `
                    <div style="max-height: 300px; overflow-y: auto;">
                    <table style="width:100%; border-collapse: collapse; text-align:left;">
                        <thead>
                            <tr style="background:#f2f2f2; border-bottom: 2px solid #ddd;">`;
            
                // Agregar encabezados en el nuevo orden
                fixedOrder.forEach(col => {
                    tableHTML += `<th style="padding: 8px; border: 1px solid #ddd;">${col}</th>`;
                });
                tableHTML += `</tr></thead><tbody>`;
            
                // Agregar filas con datos reorganizados
                reorderedRows.forEach(row => {
                    tableHTML += "<tr>";
                    row.forEach(value => {
                        tableHTML += `<td style="padding: 8px; border: 1px solid #ddd;">${value}</td>`;
                    });
                    tableHTML += "</tr>";
                });
            
                tableHTML += "</tbody></table></div>";
            
                // Mostrar SweetAlert con la tabla generada
                Swal.fire({
                    html: tableHTML,
                    confirmButtonText: "Cerrar",
                    width: "80%",
                    heightAuto: false,
                });
            
            } else {
                Swal.fire({
                    title: "Ops",
                    text: data.message,
                    icon: "warning",
                    confirmButtonText: 'Cerrar',
                    heightAuto: false,
                });
            }
        })
        .catch(error => {
            console.error('Error en la solicitud:', error);
            Swal.fire({
                title: "Error",
                text: "Ocurrió un error al procesar la solicitud.",
                icon: "error",
                confirmButtonText: 'Cerrar',
                heightAuto: false,
            });
        });


}