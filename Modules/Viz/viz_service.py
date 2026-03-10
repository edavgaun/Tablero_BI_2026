# ... (Dentro de render_map_and_waffle)

        with col_waffle:
            st.markdown(f"#### {seleccion}")
            if sum(valores_waffle) > 0:
                fig = plt.figure(
                    FigureClass=Waffle,
                    rows=n_rows,
                    values=valores_waffle,
                    colors=["#2ecc71", "#e74c3c", "#3498db", "#95a5a6"],
                    icons='bicycle', 
                    font_size=f_size, 
                    figsize=(8, 12), # Reducimos un poco el alto para que no estire de más
                    legend={
                        'labels': ['Disp', 'Dañ', 'Libre', 'Dañ'], 
                        'loc': 'lower center', 
                        'bbox_to_anchor': (0.5, -0.15), 
                        'ncol': 2, 
                        'fontsize': 11, 
                        'frameon': False
                    }
                )
                
                # AJUSTE DE MÁRGENES INTERNOS
                # right=0.95 da ese pequeño borde a la derecha
                # bottom=0.2 asegura que la leyenda tenga su propio aire
                plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.2)
                
                st.pyplot(fig, use_container_width=True, bbox_inches='tight')
                st.caption(f"**Escala:** {escala}")
